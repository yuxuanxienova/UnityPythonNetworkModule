using System;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class SocketClient : MonoBehaviour
{
    TcpClient client;
    NetworkStream stream;

    void Start()
    {
        ConnectToServer("127.0.0.1", 65432);
        SendMessageToServer("Hello from Unity!");
    }

    void ConnectToServer(string server, int port)
    {
        try
        {
            // Create a TcpClient
            client = new TcpClient(server, port);
            // Get a client stream for reading and writing
            stream = client.GetStream();
            Debug.Log("Connected to the server!");
        }
        catch (Exception e)
        {
            Debug.LogError("Error: " + e.Message);
        }
    }

    void SendMessageToServer(string message)
    {
        if (stream == null) return;

        // Translate the passed message into ASCII and store it as a Byte array
        byte[] data = Encoding.ASCII.GetBytes(message);
        stream.Write(data, 0, data.Length);
    }

    void OnApplicationQuit()
    {
        stream.Close();
        client.Close();
    }
}
