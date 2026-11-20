// Start the two original recordings together without changing either playback rate.
document.querySelectorAll('[data-video-comparison]').forEach(group => {
  const button = group.querySelector('[data-play-comparison]');
  const videos = [...group.querySelectorAll('video')];
  const isPlaying = () => videos.some(video => !video.paused && !video.ended);
  const update = () => { button.textContent = isPlaying() ? 'Pause both' : 'Play both'; };
  button.addEventListener('click', () => {
    if (isPlaying()) videos.forEach(video => video.pause());
    else videos.forEach(video => {
      video.currentTime = 0;
      video.play().catch(() => update());
    });
  });
  videos.forEach(video => ['play', 'pause', 'ended'].forEach(event => video.addEventListener(event, update)));
});
