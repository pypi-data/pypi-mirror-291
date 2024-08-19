import yt_dlp
import os
import re
import os.path as path
import requests
import shutil

class YouTubeDownloader:
    def __init__(self, root_dir, channel_handle, project_dir, genesis_playlist, revelation_playlist):
        self.root_dir = root_dir
        self.channel_url = f'https://www.youtube.com/@{channel_handle}/playlists'
        self.project_dir_path = path.join(self.root_dir, project_dir)
        # Ensure the top-level directory exists
        os.makedirs(self.root_dir, exist_ok=True)
        os.makedirs(self.project_dir_path, exist_ok=True)
        self.playlist_pattern = self.create_books_playlist_regular_expression(genesis_playlist, revelation_playlist)
        self.overwrite = False # overwrite files existing in project_ir
        self.url = 'https://audio-bible.github.io/info/books_mapping.json'

    def remove_tmp_files(self, dir=None):
        if dir is None:
          dir = self.project_dir_path
        for root, dirs, files in os.walk(self.project_dir_path):
            for file in files:
                if ".temp." in file:  # Check if ".temp." is part of the filename
                    file_path = os.path.join(root, file)  # Construct the full file path
                    try:
                        os.remove(file_path)  # Attempt to remove the file
                        print(f"Deleted: {file_path}")  # Optional: Print the path of the deleted file
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")  # Optional: Print an error message if deletion fails

    
    # if possible, create the patter dynamically to fit the last case
    def create_books_playlist_regular_expression(self, genesis_playlist, revelation_playlist):
        # Define regex to match one or more digits
        number_regex = r'\\d+'

        # Replace all sets of numbers with the number regex pattern
        pattern1 = re.sub(r'\d+', number_regex, genesis_playlist)
        pattern2 = re.sub(r'\d+', number_regex, revelation_playlist)

        # Replace specific book names with regex patterns
        pattern1 = pattern1.replace("Genesis", ".+")
        pattern2 = pattern2.replace("Revelation", ".+")

        if pattern1 == pattern2:
            return pattern1.replace("(","\(").replace(")","\)")
        else:
            # Raise an exception if patterns are not identical
            raise ValueError("Patterns do not match")


    def sanitize_title(self, title):
        # Remove trailing spaces and replace other spaces with underscores
        title = title.strip()
        title = re.sub(r'\s+', '_', title)  # Replace multiple spaces with single underscore
        return title

    def download_video(self, url, download_dir):
        def progress_hook(d):
            if d['status'] == 'error':
                print(f"Failed to download {url}: {d['error']}")

        ydl_opts = {
            'quiet': False,
            'format': 'bestaudio/best',  # Download the best audio quality
            'extractaudio': True,  # Extract audio only
            'audioformat': 'm4a',  # Desired audio format
            'audioquality': '0',  # Best audio quality
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),  # Save files in the given directory
            'noplaylist': True,  # Do not download the entire playlist
            'progress_hooks': [progress_hook],  # Add progress hooks for error handling
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    def get_expected_chapters_from_title(self, title):
        # Example function to return an expected number of chapters
        return 100

    def count_files_in_directory(self, directory_path=None):
      if directory_path is None:
        directory_path = self.project_dir_path
      total_files = 0
      
      # Walk through the directory
      for root, dirs, files in os.walk(directory_path):
          total_files += len(files)
      
      return total_files

    def list_and_process_playlists(self, reverse=False):
        ydl_opts = {
            'quiet': True,  # Suppress output to keep the script clean
            'extract_flat': True,  # Only get basic information, no downloads
            'force_generic_extractor': True,  # Handle generic extractors for playlist info
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.channel_url, download=False)

            # Extract playlists
            playlists = info_dict.get('entries', [])
            if reverse:
                playlists.reverse()  # Reverse the list to get the most recent playlist first

            for playlist in playlists:
                title = playlist.get('title', 'No Title')
                url = playlist.get('url', 'No URL')

                # Check if title matches the pattern
                if re.match(self.playlist_pattern, title): ## How to use self.pattern here?
                    # Sanitize title and create directory
                    sanitized_title = self.sanitize_title(title.replace(' (KJV)', ''))
                    directory_path = path.join(self.project_dir_path, sanitized_title)
                    os.makedirs(directory_path, exist_ok=True)

                    # Ensure existing files are not re-downloaded
                    # existing_files = set(os.listdir(directory_path))
                    existing_files = set()
                    self.remove_tmp_files(directory_path)
                    for filename in os.listdir(directory_path):
                        # Remove file extension from existing files
                        base_name, _ = os.path.splitext(filename)
                        existing_files.add(base_name)


                    print(f"Processing Playlist Title: {title}")


                    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}) as ydl:
                        info_dict = ydl.extract_info(url, download=False)
                        entries = info_dict.get('entries', [])
                        unique_titles = {entry.get('title', 'No Title') for entry in entries}
                        # expected_chapters = len(entries)
                        expected_chapters = len(unique_titles)
                        print(f" {len(existing_files)} of {expected_chapters} expected chapters")
                        if expected_chapters > 0:
                          # Check if the number of existing files matches the expected chapters
                          if len(existing_files) >= expected_chapters:
                              print(f"Skipping Playlist Title: {title} (Already has {expected_chapters} chapters)")
                              print("-" * 40)
                              continue
                        for entry in entries:
                            video_title = entry.get('title', 'No Title')# + '.mp3'
                            video_url = entry.get('url', 'No URL')
                            if video_title not in existing_files:
                                self.download_video(video_url, directory_path)
                            else:
                                print(f"Skipping already existing video: {video_title}")
                    print("-" * 40)
                else:
                    print(f"Ignored Playlist Title: {title}")
                    print(f"Playlist URL: {url}")
                    print("-" * 40)

    def version(self, version):
        self.bibleVersion = version
        return self 
    def voice(self, voice):
        self.versionName = voice
        return self 
    def result_dir(self, dir):
        self.outputDir = dir
        return self 
    
    def process(self):
        # loop through subdirectories in self.project_dir
        for dir in os.listdir(self.project_dir_path):
            dir_path = os.path.join(self.project_dir_path, dir)
            if os.path.isdir(dir_path):
              dir_name = os.path.basename(dir_path)
              bookNumber = self.getBookNumber(dir_path)
              bookName = self.getBookName(bookNumber)

              # loop through the files of this directory
              for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                  fileName = os.path.basename(file_path)
                  chapterNumber = self.getChapterNumber(fileName)
                  file_extension = os.path.splitext(fileName)[-1]

                  chapterDirectory = path.join(self.root_dir, self.outputDir, bookName.replace(' ', '_'), str(chapterNumber).zfill(3), self.bibleVersion)
                  os.makedirs(chapterDirectory, exist_ok=True)
                  chapterOutputPath = path.join(self.root_dir, self.outputDir, bookName.replace(' ', '_'), str(chapterNumber).zfill(3), self.bibleVersion, f"{self.versionName}{file_extension}")
                  # if self.force is true or chapterOutputPath does not exist, copy file_path to chapterOutputPath
                  if self.overwrite or not os.path.exists(chapterOutputPath):
                    shutil.copy2(file_path, chapterOutputPath)
                    print(f"Copied to {chapterOutputPath}")
                  else:
                    print(f"Skipping existing file: {chapterOutputPath} from {file_path}")

    def getBookNumber(self, dirName):
        # return the first set of digits with leading zeros so it is 2 digits in total
        chapterNumber = re.search(r'(\d{2})', dirName)
        if chapterNumber:
            return chapterNumber.group(1)
        else:
         raise ValueError(f"No chapter number found in {dirName}")

    def getBookName(self, chapterNumber):
        try:
            # Download the JSON file from the URL
            response = requests.get(self.url)
            response.raise_for_status()  # Check for HTTP errors

            # Parse the JSON data
            data = response.json()

            # Find and return the book name corresponding to the chapterNumber
            # Assuming the JSON structure is something like { "chapterNumber": "BookName", ... }
            return data.get(str(chapterNumber), 'Book not found')

        except requests.RequestException as e:
            # Handle potential errors in downloading or parsing
            print(f"Error fetching or parsing the JSON file: {e}")
            return None
    def force(self, force):
      self.overwrite = force 
      return self

    def getChapterNumber(self, fileName):
      # return the first set of digits with leading zeros so it is 2 digits in total
      chapterNumber = re.search(self._chapterPattern, fileName)
      if chapterNumber:
          return chapterNumber.group(1)
      else:
       raise ValueError(f"No chapter number found in {fileName} using {self._chapterPattern}")

    def chapterPattern(self, chapterPattern):
      self._chapterPattern = chapterPattern
      return self

    def download_youtube_audio(self, url, output_dir):
        # Define the download options
        ydl_opts = {
            'format': 'bestaudio/best',    # Download the best audio quality
            'extractaudio': True,          # Extract audio only
            'audioformat': 'mp3',          # Convert to MP3 format
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',  # Output file template
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
                'preferredcodec': 'mp3',      # Preferred audio codec
                'preferredquality': '192',    # Quality of the MP3 file
            }],
            'noplaylist': True,            # Download only the single video
        }

        # Create a downloader instance
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
