```mermaid
sequenceDiagram
    autonumber
    actor UserX
    participant Cloud
    participant Device
    Note over UserX,Device: Initially there is only one user, userA, who is associated with the device. The cloud broker is cloudB; it records that the device has permission too.


    alt UserX exists
        UserX->>Cloud: The user asks the cloud to publish a toggle message
        opt The cloud buffer is empty and the user has permission
            Note over Cloud: Store the toggle message in the cloud buffer.
            Cloud-->>UserX: The cloud acknowledges receipt of the message to the user
        end
    end

    alt The user currently has permission at the cloud
        Cloud->>Cloud: The cloud revokes the user’s permission
        Note over Cloud: Revoke the user’s permission.
    end

    alt UserX exists
        UserX->>Cloud: The user asks the cloud to release the buffered message
        opt The cloud has a buffered message and the device still has permission
            Note over Cloud: Clear the cloud buffer.
            Cloud->>Device: The cloud publishes the buffered message to the device
            alt The message is toggle and the device is off
                Note over Device: Turn the device on.
            else Otherwise
                Note over Device: The device ignores the message.
            end
        end
    end
```
