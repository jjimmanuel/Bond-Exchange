/**
 * To write this, I did not end up using AI as it was basically a copy/paste of the Email and SNS services, implementing the NotificationMedium Interface. 
 * As a result, it was a very straightforward thing to do, so GenAI was not used. Plus, I didn't want GenAI to make any code re-writes where it wasn't necessary, thereby avoiding violations of the 
 * assignment guidelines.
 */

import java.util.ArrayList;
import java.util.List;

/**
 * A concrete implementation of {@link NotificationMedium} for sending WhatsApp messages.
 * * @author Judah Immanuel
 * @version 1.0
 */
public class WhatsAppService implements NotificationMedium {
    /**
     * Simulates sending a WhatsApp message by printing to the standard output.
     * * @param message The text message to be dispatched.
     */
    @Override
    public void send(String message) {
        System.out.println("[WhatsApp] Sending message: " + message);
    }
}