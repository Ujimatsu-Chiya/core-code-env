#!/bin/bash

# Check if JAVA_HOME is set
if [ -z "$JAVA_HOME" ]; then
    echo "JAVA_HOME is not set. Checking for Java installation..."

    # Try to locate Java using 'which java'
    JAVA_BIN=$(which java)
    if [ -n "$JAVA_BIN" ]; then
        echo "Java found at $JAVA_BIN. Setting JAVA_HOME..."

        # Derive JAVA_HOME from the real path of the Java binary
        REAL_JAVA_PATH=$(readlink -f "$JAVA_BIN")
        JAVA_HOME=$(dirname $(dirname "$REAL_JAVA_PATH"))
        export JAVA_HOME

        # Persist JAVA_HOME and PATH to .bashrc for future sessions
        if ! grep -q "export JAVA_HOME=$JAVA_HOME" ~/.bashrc; then
            echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
            echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc
            echo "JAVA_HOME and PATH have been persisted to .bashrc."
        fi

        echo "JAVA_HOME is set to $JAVA_HOME"
    else
        echo "Java is not installed. Installing OpenJDK 21..."

        # Update package list and install OpenJDK 21
        sudo apt update
        sudo apt install -y openjdk-21-jdk

        # Verify if Java installation was successful
        JAVA_BIN=$(which java)
        if [ -n "$JAVA_BIN" ]; then
            # Derive JAVA_HOME from the real path of the Java binary
            REAL_JAVA_PATH=$(readlink -f "$JAVA_BIN")
            JAVA_HOME=$(dirname $(dirname "$REAL_JAVA_PATH"))
            export JAVA_HOME

            # Persist JAVA_HOME and PATH to .bashrc for future sessions
            if ! grep -q "export JAVA_HOME=$JAVA_HOME" ~/.bashrc; then
                echo "export JAVA_HOME=$JAVA_HOME" >> ~/.bashrc
                echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc
                echo "JAVA_HOME and PATH have been persisted to .bashrc."
            fi

            echo "OpenJDK 21 installed successfully. JAVA_HOME is set to $JAVA_HOME"
        else
            echo "Failed to install OpenJDK 21. Please check your package manager."
            exit 1
        fi
    fi
else
    echo "JAVA_HOME is already set to $JAVA_HOME"
fi

# Output the current JAVA_HOME and Java version
source ~/.bashrc # Reload .bashrc to ensure changes take effect
echo "JAVA_HOME: $JAVA_HOME"
echo "PATH: $PATH"
java -version

