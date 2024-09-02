function playMovie(movieUrl, movieFile) {
    const playerDiv = document.getElementById("player");
    const videoPlayer = videojs(document.getElementById("video-player"));
    const subsSelect = document.getElementById("subs");

    videoPlayer.src({ type: "video/mp4", src: movieUrl });
    videoPlayer.load();

    playerDiv.style.display = "block";

    fetchSubtitles(movieFile);
  }

  function fetchSubtitles(movieFile) {
    const subsSelect = document.getElementById("subs");
    subsSelect.innerHTML = '<option value="">None</option>';

    const movieBase = movieFile.split(".").slice(0, -1).join(".");

    fetch("/get_subtitles?movie=" + movieBase)
      .then((response) => response.json())
      .then((subtitles) => {
        subtitles.forEach((sub) => {
          const option = document.createElement("option");
          option.value = sub;
          option.text = sub.split("/").pop();
          subsSelect.add(option);
        });
      });
  }
  
  function addSubtitles() {
    const videoPlayer = videojs(document.getElementById("video-player"));
    const subsSelect = document.getElementById("subs");
    const subtitleUrl = subsSelect.value;

    // Elimină orice subtitrare existentă
    const tracks = videoPlayer.remoteTextTracks();
    while (tracks.length > 0) {
        videoPlayer.removeRemoteTextTrack(tracks[0]);
    }

    if (subtitleUrl) {
        const track = videoPlayer.addRemoteTextTrack(
            {
                kind: "subtitles",
                src: subtitleUrl,
                srclang: "ro",
                label: "Subtitles", // Numele modificat al subtitrării
                default: true,
            },
            false
        ).track;

        // Setează subtitrarea ca fiind activă imediat după adăugare
        track.mode = 'showing'; 
    }

    videoPlayer.play(); // Redă video-ul după ce subtitrarea a fost adăugată
}
