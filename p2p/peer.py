import sys
import socket
import struct
import threading
import time
import traceback


class Peer:
    """
    Baseado em: http://cs.berry.edu/~nhamid/p2p/
    """
    def __init__(self, server_host, server_port, max_peers=5):
        self.max_peers = int(max_peers)
        self.server_port = int(server_port)
        self.server_host = server_host
        self.my_id = '%s:%d' % (self.server_host, self.server_port)

        self.peers = {}
        self.active = False

        self.handlers = {}
        self.router = None



    def __handle_peer(self, clientsock):
        host, port = clientsock.get_peername()
        peerconn = PeerConnection(None, host, port, clientsock)
        
        msgtype, msgdata = peerconn.recvdata()
        
        self.handlers[ msgtype ](peerconn, msgdata)
        peerconn.close()


    def add_peer(self, peer_id, host, port):
        if peer_id not in self.peers and (self.max_peers == 0 or len(self.peers) < self.max_peers):
            self.peers[ peer_id ] = (host, int(port))
            return True
        else:
            return False


    def get_peer(self, peer_id):
        assert peer_id in self.peers
        return self.peers[ peer_id ]


    def remove_peer(self, peer_id):
        if peer_id in self.peers:
            del self.peers[ peer_id ]


    def get_peer_ids(self):
        return self.peers.keys()


    def makeserversocket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s


    def sendtopeer(self, peer_id, msgtype, msgdata, waitreply=True):
        if self.router:
            nextpid, host, port = self.router(peer_id)
        if not self.router or not nextpid:
            return None
        return self.connectandsend(host, port, msgtype, msgdata,
                                    pid=nextpid,
                                    waitreply=waitreply)
    

    def connectandsend(self, host, port, msgtype, msgdata, 
                        pid=None, waitreply=True):
        msgreply = []
        try:
            peerconn = PeerConnection(pid, host, port)
            peerconn.senddata(msgtype, msgdata)
            
            if waitreply:
                onereply = peerconn.recvdata()
                while (onereply != (None,None)):
                    msgreply.append(onereply)
                    onereply = peerconn.recvdata()
            peerconn.close()
        except KeyboardInterrupt:
            raise
        
        return msgreply


    def checklivepeers(self):
        todelete = []
        for pid in self.peers:
            isconnected = False
            try:
                host,port = self.peers[pid]
                peerconn = PeerConnection(pid, host, port)
                peerconn.senddata('PING', '')
                isconnected = True
            except:
                todelete.append(pid)
            if isconnected:
                peerconn.close()

        self.peerlock.acquire()
        try:
            for pid in todelete: 
                if pid in self.peers: del self.peers[pid]
        finally:
            self.peerlock.release()



    def mainloop(self):
        s = self.makeserversocket(self.server_port)
        s.settimeout(200)
        
        while not self.active:
            try:
                print 'Executando peer...'
                clientsock, clientaddr = s.accept()
                clientsock.settimeout(None)

                t = threading.Thread(target = self.__handle_peer,
                                      args = [ clientsock ])
                t.start()
            except KeyboardInterrupt:
                print 'Execucao interrompida pelo usuario'
                self.active = True
                continue

        s.close()



class PeerConnection:

    def __init__(self, peer_id, host, port, sock=None):

        self.id = peer_id

        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock

        self.sd = self.s.makefile('rw', 0)


    def __makemsg(self, msgtype, msgdata):
        msglen = len(msgdata)
        msg = struct.pack("!4sL%ds" % msglen, msgtype, msglen, msgdata)
        return msg


    def senddata(self, msgtype, msgdata):
        try:
            msg = self.__makemsg(msgtype, msgdata)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        return True
            

    def recvdata(self):
        try:
            msgtype = self.sd.read(4)
            if not msgtype: return (None, None)
            
            lenstr = self.sd.read(4)
            msglen = int(struct.unpack("!L", lenstr)[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read(min(2048, msglen - len(msg)))
                if not len(data):
                    break
                msg += data

            if len(msg) != msglen:
                return (None, None)

        except KeyboardInterrupt:
            raise
        
        return (msgtype, msg)


    def close(self):
        self.s.close()
        self.s = None
        self.sd = None


    def __str__(self):
        return "|%s|" % peer_id


if __name__=='__main__':
   if len(sys.argv) < 4:
      print "Syntax: %s hostname porta peer-ip:port" % sys.argv[0]
      sys.exit(-1)

   server_port = int(sys.argv[2])
   max_peers = 1
   peer_id = sys.argv[1] + ':' + sys.argv[2]
   peer = Peer(sys.argv[1], sys.argv[2])
   peer.mainloop()
