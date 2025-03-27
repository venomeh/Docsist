import { useState, useCallback } from "react"
import { LiveKitRoom, RoomAudioRenderer } from "@livekit/components-react"
import "@livekit/components-styles"
import SimpleVoiceAssistant from "./SimpleVoiceAssistant"

const LiveKitModal = ({ setShowSupport }) => {

    const [isSubmittingName, setIsSubmittingName] = useState(true);
    const [name, setName] = useState("");

    const handleNameSubmit = () => {
        setIsSubmittingName(false);
    }


    return <div className="modal-overlay">
        <div className="modal-content">
            <div className="support-room">
                {isSubmittingName ? (
                    <form onSubmit={handleNameSubmit} className="name-form">
                        <h2> Enter your name to connect with support</h2>
                        <input 
                            type="text" 
                            value={name} 
                            onChange={(e) => setName(e.target.value)} 
                            placeholder="Your name" 
                            required 
                        />
                        <button type="submit">Connect</button>
                        <button 
                            type="button" 
                            className="cancel-button"
                            onClick={()=>setShowSupport(false)}> 
                            Cancel
                        </button>
                    </form>
                ) : (
                    <LiveKitRoom
                        serverUrl={import.meta.env.VITE_LIVEKIT_URL}
                        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDMxMDcwOTgsImlzcyI6IkFQSUFyaG9CTW5VYmRwdCIsIm5iZiI6MTc0MzEwNjE5OCwic3ViIjoidmVub20iLCJ2aWRlbyI6eyJjYW5QdWJsaXNoIjp0cnVlLCJjYW5QdWJsaXNoRGF0YSI6dHJ1ZSwiY2FuU3Vic2NyaWJlIjp0cnVlLCJyb29tIjoiZG9jc2lzdF9yMSIsInJvb21Kb2luIjp0cnVlfX0.olfzfOKf202UjQEfejaZqzgXE0uzvcRpm5UBOtjfx2A"
                        connect={true}
                        video={false}
                        audio={true}
                        onDisconnected={()=>{
                            setShowSupport(false)
                            setIsSubmittingName(true)
                        }} 
                    >
                        <RoomAudioRenderer/>
                        <SimpleVoiceAssistant/>
                    </LiveKitRoom>
                )}
            </div>
        </div>
    </div>
}

export default LiveKitModal