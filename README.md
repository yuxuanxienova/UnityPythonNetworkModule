# General Unity Python Network Module

## Project Structure

The following is the structure of the project:

```bash
.
├── Assets/
│   ├── Scenes
│   └── Scirpts/
│           |——— Client_cs/
|           |       |___ t1_TestSimpleClient
|           |       |___ t2_TestAsyncSelectClient #Use Client Code here 
|           |___ Server_python/
│                   |___ t1_TestSimpleServer
│                   |___ t2_TestAsyncSelectClient #Use Server Code here
├── README.md              

#Unity Client
./Assets/Scripts/Client_cs/t2_TestAsyncSelectClient
|___ proto
|      |___ Messages.cs
|___ ByteArray.cs
|___ Client.cs
|___ MsgBase.cs
|___ NetManager.cs

#Python Server
./Assets/Scripts/Server_python/t2_TestAsyncSelectServer
|___ net
|    |___ __init__.py
|    |___ ByteArray.py
|    |___ ClientState.py
|    |___ MagBase.py
|    |___ NetManager.py
|___ proto
|    |___ __init__.py
|    |___ Messages.py
|___ run_server.py
|___ test_MsgBase.py
```

## Python Server
### Setup Receiving and Handling a Custom Message

In ./Assets/Scripts/Server_python/t2_TestAsyncSelectServer/proto/Message.py define the message:

```python
class MsgTest(MsgBase):
    def __init__(self):
        super().__init__()
        self.protoName = "MsgTest"
        self.str = ""
        self.num = 0
```

In ./Assets/Scripts/Client_cs/t2_TestAsyncSelectClient/proto/Messages.cs define the same message:

```c#
public class MsgTest : MsgBase
{
    public MsgTest() { protoName = "MsgTest"; }
    public string str;
    public int num;
}
```
In ./Assets/Scripts/Server_python/t2_TestAsyncSelectServer/net/NetManager.py define the message handling logic:

```python
#Under MsgHandler Class
class MsgHandler:
    @staticmethod
    def MsgPing(client:ClientState, msg_base):
        print("MsgPing")
        client.last_ping_time = NetManager.get_time_stamp()
        msg_pong = MsgPong()
        NetManager.send(client, msg_pong)
    #Add the following:
    @staticmethod
    def MsgTest(client:ClientState, msg_base):
        print("[Msg Received][client:{0}]MsgTest".format(client.client_address) + msg_base.str + str(msg_base.num) )
```

### Sending Custom Message
```python
class MsgHandler:
    @staticmethod
    def MsgPing(client:ClientState, msg_base):
        print("MsgPing")
        client.last_ping_time = NetManager.get_time_stamp()
        msg_pong = MsgPong()
        NetManager.send(client, msg_pong)
        
    @staticmethod
    def MsgTest(client:ClientState, msg_base):
        print("[Msg Received][client:{0}]MsgTest".format(client.client_address) + msg_base.str + str(msg_base.num) )
        #Create the Msg instance
        msg_test = MsgTest()
        msg_test.str = "Hi from server"
        msg_test.num = 123
        #Send Message to client
        NetManager.send(client, msg_test)
```

## C# Client
### Bind the functions with button or Binding it with keyboard input
```c#

public class Client : MonoBehaviour
{
    string SERVER_HOST = "127.0.0.1";
    int SERVER_PORT = 65432;
    void Start()
    {
        NetManager.AddEventListener(NetManager.NetEvent.ConnectSucc, OnConnectSucc);
        NetManager.AddEventListener(NetManager.NetEvent.ConnectFail, OnConnectFail);
        NetManager.AddEventListener(NetManager.NetEvent.Close, OnConnectClose);

        //add listener for custom message here
        NetManager.AddMsgListener("MsgTest", OnMsgTest);
        
    }

    public void OnConnectClick()
    {
        NetManager.Connect(SERVER_HOST, SERVER_PORT);
    }

    public void OnCloseCLick() 
    {
        NetManager.Close();
    }


    public void Update()
    {
        NetManager.Update();


        if (Input.GetKeyDown(KeyCode.T))
        {

            TestMain();

        }
    }
//---------------------------------------Test------------------------------------ 
    public void TestMain()
    {
        
        MsgTest msg = new MsgTest();
        msg.str = "Hello";
        msg.num = 100;
        NetManager.Send(msg);

    }
    //Add callback here
    public void OnMsgTest(MsgBase msgBase) 
    {
        MsgTest msg = (MsgTest)msgBase;
        Debug.Log("OnMsgTest: str=" + msg.str + " num=" + msg.num);
    }

}
```

