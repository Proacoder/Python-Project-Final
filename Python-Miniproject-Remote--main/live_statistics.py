import streamlit as st
import streamlit.components.v1 as components

def show_statistics():
    st.markdown("<h2 style='text-align: center; color: #1f2937; margin-bottom: 20px;'>Live Assignment Statistics</h2>", unsafe_allow_html=True)
    
    # HTML/CSS/JS to draw 4 live circular progress rings
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: transparent;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 40px;
        min-height: 100%;
        padding: 20px;
    }
    .circle-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.3s ease;
    }
    .circle-container:hover {
        transform: scale(1.05);
    }
    .circular-progress {
        position: relative;
        height: 140px;
        width: 140px;
        border-radius: 50%;
        background: conic-gradient(#4f46e5 0deg, #f3f4f6 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transition: background 0.3s ease;
    }
    .circular-progress::before {
        content: "";
        position: absolute;
        height: 110px;
        width: 110px;
        border-radius: 50%;
        background-color: white;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .value {
        position: relative;
        font-size: 32px;
        font-weight: 700;
        color: #1f2937;
    }
    .label {
        font-size: 15px;
        font-weight: 700;
        color: #4b5563;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    /* Specific Colors */
    #cp-pending { background: conic-gradient(#ef4444 0deg, #f3f4f6 0deg); }
    #cp-hours { background: conic-gradient(#3b82f6 0deg, #f3f4f6 0deg); }
    #cp-minutes { background: conic-gradient(#10b981 0deg, #f3f4f6 0deg); }
    #cp-seconds { background: conic-gradient(#f59e0b 0deg, #f3f4f6 0deg); }
    </style>
    </head>
    <body>

    <div class="circle-container">
        <div class="circular-progress" id="cp-pending">
            <span class="value" id="val-pending">0</span>
        </div>
        <span class="label">Pending</span>
    </div>

    <div class="circle-container">
        <div class="circular-progress" id="cp-hours">
            <span class="value" id="val-hours">0</span>
        </div>
        <span class="label">Hours Left</span>
    </div>

    <div class="circle-container">
        <div class="circular-progress" id="cp-minutes">
            <span class="value" id="val-minutes">0</span>
        </div>
        <span class="label">Minutes Left</span>
    </div>

    <div class="circle-container">
        <div class="circular-progress" id="cp-seconds">
            <span class="value" id="val-seconds">0</span>
        </div>
        <span class="label">Seconds Left</span>
    </div>

    <script>
        // Set target deadline mapping to e.g., 24 hours from now
        let deadline = new Date();
        deadline.setHours(deadline.getHours() + 11); // Add hours for demo
        deadline.setMinutes(deadline.getMinutes() + 45); // Add minutes
        deadline.setSeconds(deadline.getSeconds() + 30); // Add seconds

        // Static Assignments pending logic (Set any arbitrary value out of max 10)
        let total_assignments = 3;
        let max_assignments = 10;
        document.getElementById("val-pending").textContent = total_assignments;
        document.getElementById("cp-pending").style.background = `conic-gradient(#ef4444 ${(total_assignments/max_assignments) * 360}deg, #f3f4f6 0deg)`;

        function updateTimer() {
            let now = new Date().getTime();
            let distance = deadline.getTime() - now;

            if (distance < 0) distance = 0;

            let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Update DOM text
            document.getElementById("val-hours").textContent = hours;
            document.getElementById("val-minutes").textContent = minutes;
            document.getElementById("val-seconds").textContent = seconds;

            // Colors mapping to 360 degrees: 
            // Hours (out of 24), Minutes (out of 60), Seconds (out of 60)
            document.getElementById("cp-hours").style.background = `conic-gradient(#3b82f6 ${(hours / 24) * 360}deg, #f3f4f6 0deg)`;
            document.getElementById("cp-minutes").style.background = `conic-gradient(#10b981 ${(minutes / 60) * 360}deg, #f3f4f6 0deg)`;
            document.getElementById("cp-seconds").style.background = `conic-gradient(#f59e0b ${(seconds / 60) * 360}deg, #f3f4f6 0deg)`;
        }

        setInterval(updateTimer, 1000);
        updateTimer(); // Call initially to avoid delay
    </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=250)

if __name__ == "__main__":
    st.set_page_config(page_title="Live Statistics Dashboard", layout="wide")
    show_statistics()
