package com.company.app;

import io.atomix.AtomixReplica;
import io.atomix.catalyst.transport.Address;
import io.atomix.catalyst.transport.local.LocalServerRegistry;
import io.atomix.catalyst.transport.local.LocalTransport;
import io.atomix.copycat.server.storage.Storage;
import io.atomix.copycat.server.storage.StorageLevel;
import io.atomix.group.DistributedGroup;
import io.atomix.group.LocalMember;

public class App {
    private static LocalServerRegistry registry = new LocalServerRegistry();
    private static int port;

    private static Address nextAddress() {
        return new Address("localhost", port++);
    }

    private static AtomixReplica buildReplica(Address address) {
        return AtomixReplica.builder(address)
                .withTransport(new LocalTransport(registry))
                .withStorage(new Storage(StorageLevel.MEMORY))
                .build();
    }

    public static void main(String[] args) throws Exception {

        Address address1 = nextAddress();
        AtomixReplica node1 = buildReplica(address1);

        node1.bootstrap().join();
        System.out.println("boostrap: no 1");

        DistributedGroup group = node1.getGroup("group").get();

        group.onJoin(m -> {
            System.out.println(m.id() + " entrou no grupo");
            displayGroupMembers(group);
        });

        group.onLeave(m -> {
            System.out.println(m.id() + " saiu do grupo");
            displayGroupMembers(group);
        });

        group.election().onElection(term -> {
            System.out.println(term.leader().id() + " eh o lider");
        });

        LocalMember member1 = group.join().get();

        Address address2 = nextAddress();
        AtomixReplica node2 = buildReplica(address2);

        node2.join(address1).join();
        System.out.println("node2 se afiliou");

        DistributedGroup group1 = node2.getGroup("group").get();
        LocalMember member2 = group1.join().get();

        node2.leave();
    }

    private static void displayGroupMembers(DistributedGroup group) {
        System.out.println("\nMembros do grupo");
        group.members().forEach(m -> {
            System.out.println(m.id());
        });
    }
}