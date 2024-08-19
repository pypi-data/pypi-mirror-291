<div align="center">
  
# SpotifyFizyFit
<img src="https://github.com/fleizean/spotifyfizyfit/raw/main/assets/img/spotifyfizyfit.png" >

The **Spotify to Fizy Playlist Sync Bot** is an automation tool designed to integrate Spotify playlists with Fizy. This bot fetches playlist data from Spotify and adds the tracks to corresponding playlists on Fizy. It simplifies the process of transferring music between these two platforms, ensuring your playlists are consistent across both services.

[![MIT License](https://img.shields.io/github/license/fleizean/spotifyfizyfit?color=44CC11&style=flat-square)](https://github.com/fleizean/spotifyfizyfit/blob/master/LICENSE)
[![PyPI version](https://img.shields.io/pypi/pyversions/spotifyfizyfit?color=%2344CC11&style=flat-square)](https://pypi.org/project/spotifyfizyfit/)
[![PyPi downloads](https://img.shields.io/pypi/dw/spotifyfizyfit?label=downloads@pypi&color=344CC11&style=flat-square)](https://pypi.org/project/spotifyfizyfit/)
![Contributors](https://img.shields.io/github/contributors/fleizean/spotifyfizyfit?style=flat-square)

</div>

## Installation

### Python (Recommended Method)
  - _spotifyfizyfit_ can be installed by running `pip install spotifyfizyfit`.
  - To update spotifyfizyfit run `pip install --upgrade spotifyfizyfit`

  > On some systems you might have to change `pip` to `pip3`.

  <details>
    <summary style="font-size:1.25em"><strong>Other options</strong></summary>
    - On Termux
        - `sh -c "$(curl https://raw.githubusercontent.com/fleizean/spotifyfizyfit/main/install.sh)"`      
    - Build from source
        ```bash
	    git clone https://github.com/flizean/spotifyfizyfit && cd spotifyfizyfit
        sh install.sh	    
	    ```
        Right now, enjoy it with `spotifyfizyfit`. 
  </details>

  ### Specifying JSON File Path
    During installation, you might need to specify the path to a JSON file. You can do this by setting an environment variable or passing the path as an argument to the script. For example:
  
    To get started, you need to request your data from Spotify. Please refer to the following document for detailed instructions:

    [Spotify Data Collection Guide](https://github.com/fleizean/spotifyfizyfit/blob/main/md/SpotifyCollectData.md)
    
## Usage

  To use the **Spotify to Fizy Playlist Sync Bot**, follow these steps:

  1. Install the `spotifyfizyfit` package by running the following command:
     ```
     pip install spotifyfizyfit
     ```

  2. Update the `spotifyfizyfit` package to the latest version with the following command:
     ```
     pip install --upgrade spotifyfizyfit
     ```

     > Note: On some systems, you might need to use `pip3` instead of `pip`.

    01. Specify the path to your JSON configuration file. You can do this in one of the following ways:
  
     - **Directly as a Command-Line Argument:**
       ```bash
       spotifyfizyfit /path/to/your/config.json
       ```

  3. Enjoy using `spotifyfizyfit` to sync your Spotify playlists with Fizy!

## Contributions

We welcome contributions to the SpotifyFizyFit project! If you would like to contribute, please read the [CONTRIBUTING.md](https://github.com/fleizean/spotifyfizyfit/blob/main/md/CONTRIBUTING.md) file for detailed instructions on how to get started.

Thank you for your interest in contributing to our project!

## License

This project is Licensed under the [MIT](https://github.com/fleizean/spotifyfizyfit/blob/main/LICENSE) License.