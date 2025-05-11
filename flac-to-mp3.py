import os
from pydub import AudioSegment

def convert_m3u_flac_to_mp3(playlist_path, output_playlist_path):
    # Ensure the playlist file exists
    if not os.path.isfile(playlist_path):
        print(f"Playlist file {playlist_path} not found.")
        return

    with open(playlist_path, 'r') as infile:
        lines = infile.readlines()

    # Prepare the output directory
    output_dir = os.path.join(os.path.dirname(output_playlist_path), "converted_mp3")
    os.makedirs(output_dir, exist_ok=True)

    # Process each line in the playlist
    converted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line.endswith(".flac"):
            # Copy comments or non-FLAC lines directly
            converted_lines.append(line)
            continue

        flac_path = line
        mp3_name = os.path.splitext(os.path.basename(flac_path))[0] + ".mp3"
        mp3_path = os.path.join(output_dir, mp3_name)

        try:
            # Convert FLAC to MP3
            print(f"Converting {flac_path} to {mp3_path}")
            audio = AudioSegment.from_file(flac_path, format="flac")
            audio.export(mp3_path, format="mp3", bitrate="320k")
            converted_lines.append(mp3_path)
        except Exception as e:
            print(f"Error converting {flac_path}: {e}")
            converted_lines.append(flac_path)  # Keep original if conversion fails

    # Write the new playlist
    with open(output_playlist_path, 'w') as outfile:
        outfile.write("\n".join(converted_lines))

    print(f"New playlist created at {output_playlist_path}")

# Example usage
playlist_path = "/path/to/playlist.m3u"
output_playlist_path = "/path/to/playlist.mp3.m3u"
convert_m3u_flac_to_mp3(playlist_path, output_playlist_path)
