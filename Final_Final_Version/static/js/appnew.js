function handleError(error) {
    console.error('navigator.getUserMedia error: ', error);
  }
  const constraints = {video: true};
  
  (function() {
    const video = document.querySelector('#basic video');
    const captureVideoButton = document.querySelector('#basic .capture-button');
    let localMediaStream;
  
    function handleSuccess(stream) {
      localMediaStream = stream;
      video.srcObject = stream;
    }
  
    captureVideoButton.onclick = function() {
      navigator.mediaDevices.getUserMedia(constraints).
        then(handleSuccess).catch(handleError);
    };
  
    document.querySelector('#stop-button').onclick = function() {
      video.pause();
      localMediaStream.stop();
    };
  });
  
  (function() {
    const captureVideoButton =
      document.querySelector('#screenshot .capture-button');
    const screenshotButton = document.querySelector('#screenshot-button');
    const img = document.querySelector('#screenshot img');
    const video = document.querySelector('#screenshot video');
  
    const canvas = document.createElement('canvas');
  
    captureVideoButton.onclick = function() {
      navigator.mediaDevices.getUserMedia(constraints).
        then(handleSuccess).catch(handleError);
    };
  
    screenshotButton.onclick = video.onclick = function() {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      // Other browsers will fall back to image/png
      img.src = canvas.toDataURL('image/webp');
    };
  
    function handleSuccess(stream) {
      screenshotButton.disabled = false;
      video.srcObject = stream;
    }
  })();
  
