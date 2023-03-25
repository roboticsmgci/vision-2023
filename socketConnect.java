import java.io.IOException;
import java.net.*;
public class JavaSocketConnectExample1 {
    public static void main(String[] args) throws IOException {
      Socket socket = new Socket();
      InetAddress inetAddress=InetAddress.getByName("wpilibpi.local");
      int port=8574;
      SocketAddress socketAddress=new InetSocketAddress(inetAddress, port);
      socket.bind(socketAddress);
      socket.connect(socketAddress);
      System.out.println("Inet address: "+socket.getInetAddress());
      System.out.println("Port number: "+socket.getLocalPort());
  }
}