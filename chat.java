import java.util.Scanner;
import javax.swing.*;
import java.io.*;

public class chat {
    String username;
    String password;
    String messages;
    String filePath = "Y:\\3BHIT\\test\\chat.txt";
    JTextArea chat = new JTextArea();

    private void readMessages() {
        try {
            File fp = new File(this.filePath);
            if (fp.createNewFile())
                System.out.println("File created: " + fp.getName());

            Scanner reader = new Scanner(fp);
            messages = "";
            while (reader.hasNextLine()) {
                String data = reader.nextLine();
                messages += data + "\n";
            }
            chat.setText(messages);
            chat.setCaretPosition(chat.getDocument().getLength());
            reader.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }

    private void writeMessages(String message) {
        try {
            FileWriter myWriter = new FileWriter(this.filePath, true);
            myWriter.write(message);
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }

    private void inputGUI() {
        JFrame frame = new JFrame("Moritz Tools Java");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JTextField userText = new JTextField(20);
        JLabel userLabel = new JLabel("Username");

        JPasswordField keyText = new JPasswordField(20);
        JLabel keyLabel = new JLabel("Password");
        keyText.setEchoChar('*');

        keyText.addActionListener(e -> {
            username = userText.getText();
            password = new String(keyText.getPassword());
            frame.dispose();
            createAndShowGUI();
        });

        JButton button = new JButton("Starten");
        button.addActionListener(e -> {
            username = userText.getText();
            password = new String(keyText.getPassword());
            frame.dispose();
            createAndShowGUI();
        });
        JPanel panel = new JPanel();
        panel.add(userLabel);
        panel.add(userText);
        panel.add(keyLabel);
        panel.add(keyText);
        panel.add(button);
        frame.getContentPane().add(panel);
        frame.pack();
        frame.setVisible(true);
    }

    private void createAndShowGUI() {
        JFrame frame = new JFrame("Moritz Tools Java");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        chat.setLineWrap(true);
        chat.setWrapStyleWord(true);
        chat.setEditable(false);
        frame.getContentPane().add(new JScrollPane(chat));
        frame.setSize(800, 600);
        frame.setVisible(true);

        JTextField input = new JTextField();
        input.addActionListener(e -> {
            String text = input.getText();
            chat.append(String.format("%s: %s%n", username, text));
            input.setText("");
            writeMessages(String.format("%s: %s%n", username, text));
            chat.setCaretPosition(chat.getDocument().getLength());
            readMessages();
        });
        frame.getContentPane().add(input, "South");
        SwingUtilities.invokeLater(() -> input.requestFocusInWindow());

        frame.setVisible(true);
        Timer timer = new Timer(1000, e -> readMessages());
        timer.start();
        readMessages();
    }

    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                chat app = new chat();
                app.inputGUI();
            }
        });
    }
}
