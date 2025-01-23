#!/bin/bash

# Check if GOPATH is set
if [ -z "$GOPATH" ]; then
    echo "GOPATH is not set. Checking for Go installation..."

    # Try to locate Go using 'which go'
    GO_BIN=$(which go)
    if [ -n "$GO_BIN" ]; then
        echo "Go found at $GO_BIN. Configuring environment..."

        # Set GOPATH to the default Go workspace
        GOPATH=$HOME/go
        export GOPATH
        export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin

        # Persist GOPATH and PATH to .bashrc for future sessions
        if ! grep -q "export GOPATH=$GOPATH" ~/.bashrc; then
            echo "export GOPATH=$GOPATH" >> ~/.bashrc
            echo "export PATH=\$PATH:/usr/local/go/bin:\$HOME/go/bin" >> ~/.bashrc
            echo "GOPATH and PATH have been persisted to .bashrc."
        fi

        echo "GOPATH is set to $GOPATH"
    else
        echo "Go is not installed. Installing Go from source..."

        # Define the Go version and source URL
        GO_VERSION="go1.23.5" # Update this to the desired version
        GO_SRC_URL="https://go.dev/dl/${GO_VERSION}.src.tar.gz"

        echo "Downloading Go source from $GO_SRC_URL..."
        wget $GO_SRC_URL -O /tmp/${GO_VERSION}.src.tar.gz

        echo "Extracting Go source..."
        sudo tar -C /usr/local -xzf /tmp/${GO_VERSION}.src.tar.gz

        # Build Go from source
        echo "Building Go from source..."
        cd /usr/local/go/src || { echo "Go source directory not found!"; exit 1; }
        sudo ./make.bash

        # Set up Go binary path
        export PATH=$PATH:/usr/local/go/bin
        echo "export PATH=\$PATH:/usr/local/go/bin:\$HOME/go/bin" >> ~/.bashrc

        # Set GOPATH to the default Go workspace
        GOPATH=$HOME/go
        export GOPATH
        export PATH=$PATH:$GOPATH/bin

        # Persist GOPATH and PATH to .bashrc
        if ! grep -q "export GOPATH=$GOPATH" ~/.bashrc; then
            echo "export GOPATH=$GOPATH" >> ~/.bashrc
            echo "export PATH=\$PATH:\$GOPATH/bin" >> ~/.bashrc
            echo "GOPATH and PATH have been persisted to .bashrc."
        fi

        echo "Go 1.23.5 has been installed successfully. GOPATH is set to $GOPATH"
    fi
else
    echo "GOPATH is already set to $GOPATH"
fi

# Output the current Go environment
source ~/.bashrc # Reload .bashrc to ensure changes take effect
echo "GOPATH: $GOPATH"
go version

# Try installing goimports with the default GOPROXY
echo "Attempting to install goimports with the default GOPROXY..."
if go install golang.org/x/tools/cmd/goimports@latest &> /dev/null; then
    echo "goimports installed successfully with the default GOPROXY."
else
    echo "Default GOPROXY failed. Switching to alternative GOPROXY..."

    # Set alternative GOPROXY
    GOPROXY_URL="https://goproxy.cn,direct"
    echo "Setting GOPROXY to $GOPROXY_URL"
    go env -w GOPROXY=$GOPROXY_URL

    # Retry installation
    echo "Retrying installation of goimports..."
    if go install golang.org/x/tools/cmd/goimports@latest &> /dev/null; then
        echo "goimports installed successfully after switching GOPROXY."
    else
        echo "Failed to install goimports even after switching GOPROXY. Exiting with error."
        exit 1
    fi
fi

# Get installation path
GO_BIN=$(go env GOBIN)
if [ -z "$GO_BIN" ]; then
  GO_BIN=$(go env GOPATH)/bin
fi

GOIMPORTS_PATH="$GO_BIN/goimports"

# Check if installation was successful
if [ ! -f "$GOIMPORTS_PATH" ]; then
  echo "goimports installation failed. Please check the error logs."
  exit 1
fi

echo "goimports has been successfully installed: $GOIMPORTS_PATH"

# Add GOPATH/bin to PATH if not already added
if [[ ":$PATH:" != *":$GO_BIN:"* ]]; then
  echo "Adding $GO_BIN to PATH..."
  echo "export PATH=\$PATH:$GO_BIN" >> ~/.bashrc
  source ~/.bashrc
fi

# Verify installation
if command -v goimports &> /dev/null; then
  echo "goimports installation complete. You can now use the goimports command."
else
  echo "Please check your PATH settings or restart the terminal to load the environment variables."
fi

