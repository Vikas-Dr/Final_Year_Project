import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function VerificationPage() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [idFile, setIdFile] = useState(null);
  const [selfieFile, setSelfieFile] = useState(null);
  const [idPreview, setIdPreview] = useState("");
  const [selfiePreview, setSelfiePreview] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);
  const [captureTarget, setCaptureTarget] = useState("");
  const [cameraError, setCameraError] = useState("");
  const [existingStatus, setExistingStatus] = useState(null);
  const [dragTarget, setDragTarget] = useState("");
  const [uploadError, setUploadError] = useState("");

  useEffect(() => () => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (!cameraOn || !video || !streamRef.current) return;

    video.srcObject = streamRef.current;
    video.play().catch(() => {
      setCameraError("The camera preview could not start. Check your browser’s camera permission.");
    });
  }, [cameraOn, captureTarget]);

  useEffect(() => {
    api.get("/verification/status")
      .then((res) => setExistingStatus(res.data))
      .catch(() => setExistingStatus({ status: "pending", verified: false }));
  }, []);

  useEffect(() => () => {
    if (idPreview) URL.revokeObjectURL(idPreview);
    if (selfiePreview) URL.revokeObjectURL(selfiePreview);
  }, [idPreview, selfiePreview]);

  const setUploadedImage = (file, setFile, setPreview, label) => {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setUploadError(`Choose an image file for your ${label}.`);
      return;
    }
    setFile(file);
    setPreview(URL.createObjectURL(file));
    setStatus(null);
    setUploadError("");
  };

  const handleIdUpload = (event) => {
    const file = event.target.files?.[0];
    setUploadedImage(file, setIdFile, setIdPreview, "ID");
    event.target.value = "";
  };

  const handleSelfieUpload = (event) => {
    const file = event.target.files?.[0];
    setUploadedImage(file, setSelfieFile, setSelfiePreview, "photo");
    event.target.value = "";
  };

  const handleDrop = (event, setFile, setPreview, label) => {
    event.preventDefault();
    setDragTarget("");
    setUploadedImage(event.dataTransfer.files?.[0], setFile, setPreview, label);
  };

  const closeCamera = () => {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    setCameraOn(false);
    setCaptureTarget("");
  };

  const openCamera = async (target) => {
    setCameraError("");
    setUploadError("");
    setStatus(null);
    setCaptureTarget(target);

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError("Live camera is not available in this browser. Upload an image instead.");
      return;
    }

    try {
      streamRef.current?.getTracks().forEach((track) => track.stop());
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
        audio: false,
      });
      streamRef.current = stream;
      setCameraOn(true);
    } catch (error) {
      setCameraOn(false);
      setCameraError(
        error.name === "NotAllowedError"
          ? "Camera permission is blocked. Allow camera access in your browser settings, or upload an image."
          : "Could not start the camera. Check that it is connected and not being used by another app."
      );
    }
  };

  const captureImage = () => {
    if (!videoRef.current || !captureTarget) return;

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    if (!context || !canvas.width || !canvas.height) {
      setCameraError("The camera is still starting. Wait a moment, then take the photo.");
      return;
    }

    context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (!blob) {
        setCameraError("Could not save the camera photo. Please try again.");
        return;
      }

      const isId = captureTarget === "id";
      const file = new File([blob], isId ? "id-card-capture.jpg" : "selfie-capture.jpg", { type: "image/jpeg" });
      setUploadedImage(
        file,
        isId ? setIdFile : setSelfieFile,
        isId ? setIdPreview : setSelfiePreview,
        isId ? "ID" : "photo"
      );
      closeCamera();
    }, "image/jpeg", 0.92);
  };

  const submitVerification = async () => {
    if (!idFile || !selfieFile) {
      setStatus({ verified: false, message: "Please upload both your ID card and a selfie." });
      return;
    }

    setLoading(true);
    setStatus(null);

    const formData = new FormData();
    formData.append("id_image", idFile, "id-card.png");
    formData.append("selfie_image", selfieFile, "selfie.png");

    try {
      const res = await api.post("/verification/verify", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(res.data);
    } catch (error) {
      setStatus({
        verified: false,
        message: error.response?.data?.detail || "Verification failed. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  const isVerified = Boolean(status?.verified || existingStatus?.verified);
  const verificationBadge = isVerified
    ? "Identity Verified"
    : existingStatus?.status === "rejected"
      ? "Verification Rejected"
      : "Awaiting Verification";

  return (
    <div className="verification-outer identity-verification-page">
      <section className="verification-card identity-verification-card animate-scaleIn">
        <header className="identity-verification-header">
          <div className="eyebrow">Candidate check-in</div>
          <h1>Let’s confirm it’s you.</h1>
          <p>Use your laptop camera to photograph your ID and yourself, or upload clear images instead.</p>
        </header>

        <div className="verification-steps identity-verification-steps" aria-label="Verification progress">
          <div className={`vstep ${idFile ? "done" : "active"}`} aria-current={!idFile ? "step" : undefined}>
            <div className="vstep-num">{idFile ? "✓" : "1"}</div>
            <div className="vstep-label">Identity document</div>
          </div>
          <div className={`vstep ${selfieFile ? "done" : ""} ${idFile && !selfieFile ? "active" : ""}`} aria-current={idFile && !selfieFile ? "step" : undefined}>
            <div className="vstep-num">{selfieFile ? "✓" : "2"}</div>
            <div className="vstep-label">Your photo</div>
          </div>
          <div className={`vstep ${isVerified ? "done" : ""}`} aria-current={isVerified ? "step" : undefined}>
            <div className="vstep-num">{isVerified ? "✓" : "3"}</div>
            <div className="vstep-label">Review</div>
          </div>
        </div>

        {uploadError && <div className="identity-upload-error" role="alert">{uploadError}</div>}

        <div className="identity-upload-grid">
          <section
            className={`identity-upload-panel ${dragTarget === "id" ? "is-dragging" : ""} ${idPreview ? "has-file" : ""}`}
            onDragOver={(event) => { event.preventDefault(); setDragTarget("id"); }}
            onDragLeave={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setDragTarget(""); }}
            onDrop={(event) => handleDrop(event, setIdFile, setIdPreview, "ID")}
            aria-labelledby="id-panel-title"
          >
            <div className="identity-panel-heading">
              <span className="identity-panel-index">A</span>
              <div>
                <h2 id="id-panel-title">Identity document</h2>
                <p>Hold your ID in the camera frame, or choose a clear image.</p>
              </div>
              <span className={`identity-file-state ${idFile ? "is-ready" : ""}`}>{idFile ? "Added" : "Required"}</span>
            </div>
            <div className="identity-preview-frame identity-document-frame">
              {idPreview ? (
                <img src={idPreview} alt="Preview of your identity document" />
              ) : (
                <div className="identity-empty-state">
                  <div className="identity-document-illustration" aria-hidden="true">
                    <span />
                    <i />
                    <b />
                  </div>
                  <strong>Your ID goes here</strong>
                  <span>Keep all four edges in frame</span>
                </div>
              )}
            </div>
            <div className="identity-upload-footer">
              <div className="identity-file-copy">
                <strong>{idFile ? idFile.name : "Front side of your ID"}</strong>
                <span>{idFile ? "Ready for verification" : "JPG, PNG or WebP"}</span>
              </div>
              <div className="identity-photo-actions">
                <button className="identity-file-button identity-capture-button" type="button" onClick={() => openCamera("id")}>
                  {idFile ? "Retake with camera" : "Use camera"}
                </button>
                <label className="identity-file-button" htmlFor="id-upload-input">
                  {idFile ? "Upload another" : "Upload"}
                  <input id="id-upload-input" type="file" accept="image/*" onChange={handleIdUpload} />
                </label>
              </div>
            </div>
          </section>

          <section
            className={`identity-upload-panel ${dragTarget === "selfie" ? "is-dragging" : ""} ${selfiePreview ? "has-file" : ""}`}
            onDragOver={(event) => { event.preventDefault(); setDragTarget("selfie"); }}
            onDragLeave={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setDragTarget(""); }}
            onDrop={(event) => handleDrop(event, setSelfieFile, setSelfiePreview, "photo")}
            aria-labelledby="selfie-panel-title"
          >
            <div className="identity-panel-heading">
              <span className="identity-panel-index">B</span>
              <div>
                <h2 id="selfie-panel-title">Your photo</h2>
                <p>Sit in front of your laptop and look toward the camera.</p>
              </div>
              <span className={`identity-file-state ${selfieFile ? "is-ready" : ""}`}>{selfieFile ? "Added" : "Required"}</span>
            </div>
            <div className="identity-preview-frame identity-selfie-frame">
              {selfiePreview ? (
                <img src={selfiePreview} alt="Preview of your selfie" />
              ) : (
                <div className="identity-empty-state">
                  <div className="identity-face-illustration" aria-hidden="true">
                    <span />
                    <i />
                  </div>
                  <strong>Your photo goes here</strong>
                  <span>Use the camera or upload a recent photo</span>
                </div>
              )}
            </div>
            <div className="identity-upload-footer">
              <div className="identity-file-copy">
                <strong>{selfieFile ? selfieFile.name : "A recent face photo"}</strong>
                <span>{selfieFile ? "Ready for verification" : "JPG, PNG or WebP"}</span>
              </div>
              <div className="identity-photo-actions">
                <button className="identity-file-button identity-capture-button" type="button" onClick={() => openCamera("selfie")}>
                  {selfieFile ? "Retake with camera" : "Use camera"}
                </button>
                <label className="identity-file-button" htmlFor="selfie-file-input">
                  {selfieFile ? "Replace" : "Upload"}
                  <input id="selfie-file-input" type="file" accept="image/*" onChange={handleSelfieUpload} />
                </label>
              </div>
            </div>
          </section>
        </div>

        {captureTarget && (
          <section className="identity-camera-capture" aria-label={captureTarget === "id" ? "Capture identity document" : "Capture selfie"}>
            <div className="identity-camera-heading">
              <div>
                <span className="identity-panel-index">{captureTarget === "id" ? "A" : "B"}</span>
                <div>
                  <h2>{captureTarget === "id" ? "Photograph your ID" : "Take your photo"}</h2>
                  <p>{captureTarget === "id" ? "Hold the ID steady inside the card outline." : "Sit facing the laptop and center your face in the oval."}</p>
                </div>
              </div>
              <button className="identity-camera-close" type="button" onClick={closeCamera}>Cancel</button>
            </div>
            {cameraError ? (
              <div className="identity-camera-error" role="alert">{cameraError}</div>
            ) : (
              <div className="identity-camera-frame">
                <video
                  ref={videoRef}
                  className={captureTarget === "selfie" ? "is-selfie" : ""}
                  autoPlay
                  playsInline
                  muted
                />
                <div className={captureTarget === "id" ? "identity-id-guide" : "identity-face-guide"} aria-hidden="true" />
                <span className="identity-camera-live"><i /> Live camera</span>
              </div>
            )}
            {cameraError ? (
              <button className="identity-camera-retry" type="button" onClick={() => openCamera(captureTarget)}>
                Try camera again
              </button>
            ) : (
              <button className="primary-button identity-camera-shutter" type="button" onClick={captureImage} disabled={!cameraOn}>
                Take {captureTarget === "id" ? "ID photo" : "selfie"}
              </button>
            )}
          </section>
        )}

        <div className="identity-verification-bottom">
          <div className="identity-status-row">
            <div className={`identity-status-mark ${isVerified ? "is-verified" : ""}`} aria-hidden="true">{isVerified ? "✓" : "·"}</div>
            <div>
              <strong>{verificationBadge}</strong>
              <span>{isVerified ? "You’re ready to continue." : "Your images are only sent when you start verification."}</span>
            </div>
            {existingStatus?.score ? <span className="identity-match-score">{Number(existingStatus.score).toFixed(2)} match</span> : null}
          </div>
          <button className="primary-button identity-submit-button" type="button" onClick={submitVerification} disabled={loading || !idFile || !selfieFile}>
            {loading ? "Checking your details…" : "Verify identity"}
            {!loading && <span aria-hidden="true">→</span>}
          </button>
        </div>

        {status && (
          <div className={`verify-result ${status.verified ? "success" : "fail"} identity-verify-result`} role="status" aria-live="polite">
            <div className="verify-score-big">{status.score ? Number(status.score).toFixed(2) : "0.00"}</div>
            <div>
              <strong>{status.verified ? "Identity confirmed" : "We couldn’t confirm your identity"}</strong>
              <p>{status.message || "Verification result."}</p>
            </div>
          </div>
        )}

        {isVerified && (
          <div className="identity-next-steps">
            <Link to="/resume-analysis" className="primary-button">Continue to resume analysis <span aria-hidden="true">→</span></Link>
            <Link to="/interview" className="secondary-button">Enter interview room</Link>
          </div>
        )}
      </section>
    </div>
  );
}
