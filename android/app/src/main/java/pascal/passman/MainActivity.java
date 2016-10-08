package pascal.passman;

import android.content.DialogInterface;
import android.os.SystemClock;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import android.content.Context;
import android.content.ClipboardManager;
import android.text.InputType;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.lambdaworks.crypto.SCrypt;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public String result;

    public void sayHello(View v) {


        EditText passField = (EditText)findViewById(R.id.editText);
        EditText keyField = (EditText)findViewById(R.id.editText2);

        try {
            result = "!A" + bytesToHex(SCrypt.scrypt(passField.getText().toString().getBytes("UTF-8"), keyField.getText().toString().getBytes("UTF-8"), 32768, 8, 1, 32)).substring(0, 30).toLowerCase();
        } catch (java.security.GeneralSecurityException e) {
            result = "WronK";
        } catch (java.io.UnsupportedEncodingException e) {
            result = "encoding";
        };

        //progressBar.setVisibility(View.INVISIBLE);
        copyToClipboard(result);
    }


    final protected static char[] hexArray = "0123456789ABCDEF".toCharArray();
    public static String bytesToHex(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 2];
        for ( int j = 0; j < bytes.length; j++ ) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = hexArray[v >>> 4];
            hexChars[j * 2 + 1] = hexArray[v & 0x0F];
        }
        return new String(hexChars);
    }

    public void copyToClipboard(String copyText) {
            android.content.ClipboardManager clipboard = (android.content.ClipboardManager)
                    getSystemService(Context.CLIPBOARD_SERVICE);
            android.content.ClipData clip = android.content.ClipData
                    .newPlainText("Your OTP", copyText);
            clipboard.setPrimaryClip(clip);

        Toast toast = Toast.makeText(getApplicationContext(),
                "Your OTP is copied",
                Toast.LENGTH_SHORT);
        toast.setGravity(Gravity.BOTTOM | Gravity.RIGHT, 50, 50);
        toast.show();
        finish();
        //displayAlert(copyText);
    }

}