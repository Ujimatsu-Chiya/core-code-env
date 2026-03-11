package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

const (
	READ_PATH  = "user.in"
	WRITE_PATH = "user.out"
)

type StdinWrapper struct {
	scanner *bufio.Scanner
}

func CreateStdinWrapper() *StdinWrapper {
	file, err := os.Open(READ_PATH)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening input file: %v\n", err)
		os.Exit(1)
	}
	return &StdinWrapper{
		scanner: bufio.NewScanner(file),
	}
}

func (s *StdinWrapper) ReadLine() string {
	if s.scanner.Scan() {
		line := strings.TrimSpace(s.scanner.Text())
		return line
	}
	if err := s.scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Error reading input file: %v\n", err)
		os.Exit(1)
	}
	return ""
}

type StdoutWrapper struct {
	writer *bufio.Writer
}

func CreateStdoutWrapper() *StdoutWrapper {
	file, err := os.Create(WRITE_PATH)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creating output file: %v\n", err)
		os.Exit(1)
	}
	return &StdoutWrapper{
		writer: bufio.NewWriter(file),
	}
}

func (s *StdoutWrapper) WriteLine(line string) {
	_, err := s.writer.WriteString(line + "\n")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error writing to output file: %v\n", err)
		os.Exit(1)
	}
	if err := s.writer.Flush(); err != nil {
		fmt.Fprintf(os.Stderr, "Error flushing output file: %v\n", err)
		os.Exit(1)
	}
}