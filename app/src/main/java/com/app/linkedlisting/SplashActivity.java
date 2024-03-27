package com.app.linkedlisting;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthInvalidCredentialsException;
import com.google.firebase.auth.FirebaseAuthInvalidUserException;
import com.google.firebase.auth.FirebaseUser;

public class SplashActivity extends AppCompatActivity {

    private FirebaseAuth mAuth;
    private EditText emailEditText, passwordEditText;
    private Button loginButton, signupButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        mAuth = FirebaseAuth.getInstance();

        emailEditText = findViewById(R.id.usernameOrEmailEditText);
        passwordEditText = findViewById(R.id.passwordEditText);
        loginButton = findViewById(R.id.loginButton);
        signupButton = findViewById(R.id.signupButton);

        loginButton.setOnClickListener(v -> loginUser());
        signupButton.setOnClickListener(v -> {
            // Navigate to SignUpActivity for new user registration
            Intent signupIntent = new Intent(SplashActivity.this, SignUpActivity.class);
            startActivity(signupIntent);
        });

        // Automatically attempt to log in if credentials are valid/saved
        autoLogin();
    }

    private void autoLogin() {
        FirebaseUser currentUser = mAuth.getCurrentUser();
        if (currentUser != null) {
            navigateToMainActivity();
        }
        // Else, stay on this activity for user to log in or sign up
    }

    private void loginUser() {
        String email = emailEditText.getText().toString().trim();
        String password = passwordEditText.getText().toString().trim();

        if (email.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Please enter both email and password.", Toast.LENGTH_SHORT).show();
            return;
        }

        mAuth.signInWithEmailAndPassword(email, password).addOnCompleteListener(this, task -> {
            if (task.isSuccessful()) {
                navigateToMainActivity();
            } else {
                // Improved error handling for specific auth failures
                handleAuthFailure(task);
            }
        });
    }

    private void handleAuthFailure(@NonNull Task<AuthResult> task) {
        String errorMessage = "Authentication failed."; // Default message

        if (task.getException() instanceof FirebaseAuthInvalidCredentialsException) {
            errorMessage = "Invalid password.";
        } else if (task.getException() instanceof FirebaseAuthInvalidUserException) {
            errorMessage = "Invalid email or user does not exist.";
        }

        Toast.makeText(SplashActivity.this, errorMessage, Toast.LENGTH_SHORT).show();
    }

    private void navigateToMainActivity() {
        Intent mainIntent = new Intent(SplashActivity.this, MainActivity.class);
        startActivity(mainIntent);
        finish();
    }
}
