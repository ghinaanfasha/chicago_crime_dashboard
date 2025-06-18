import streamlit as st

def apply_custom_styles():
    """Apply responsive custom CSS styles to the Streamlit app"""
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            /* Base responsive sidebar with animations */
            [data-testid="stSidebar"] {
                width: clamp(180px, 20vw, 250px) !important;
                padding-top: 2rem;
                min-width: 180px;
                background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
                border-right: 3px solid #8979FF !important;
                position: relative;
                overflow: hidden;
            }

            /* Animated sidebar background */
            [data-testid="stSidebar"]::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 20%, rgba(137, 121, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(137, 121, 255, 0.08) 0%, transparent 50%),
                    radial-gradient(circle at 40% 60%, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
                animation: sidebarPulse 4s ease-in-out infinite alternate;
                pointer-events: none;
                z-index: 0;
            }

            @keyframes sidebarPulse {
                0% {
                    opacity: 0.3;
                    transform: scale(1);
                }
                100% {
                    opacity: 0.7;
                    transform: scale(1.02);
                }
            }

            /* Sidebar floating decoration */
            [data-testid="stSidebar"]::after {
                content: "";
                position: absolute;
                top: 10%;
                right: -20px;
                width: 40px;
                height: 40px;
                background: linear-gradient(45deg, #8979FF, #a855f7);
                border-radius: 50%;
                animation: floatSidebar 3s ease-in-out infinite;
                opacity: 0.6;
                z-index: 0;
            }

            @keyframes floatSidebar {
                0%, 100% {
                    transform: translateY(0px) rotate(0deg);
                }
                50% {
                    transform: translateY(-10px) rotate(180deg);
                }
            }

            /* Main content area adjustments */
            .main .block-container {
                padding-left: clamp(1rem, 3vw, 2rem) !important;
                padding-right: clamp(1rem, 3vw, 2rem) !important;
                max-width: none !important;
                padding-top: 1rem !important;
            }

            [data-testid="collapsedControl"] ~ .main .block-container {
                margin-left: auto !important;
                margin-right: auto !important;
                padding-left: clamp(2rem, 8vw, 6rem) !important;
                padding-right: clamp(2rem, 8vw, 6rem) !important;
                max-width: 1200px !important;
            }

            /* Background box and animation */
            .main-title-container {
                border-radius: 20px 20px 0 0;
                padding: 2rem 1rem;
                margin: 0 0 0.5rem 0;
                box-shadow: 
                    0 20px 40px rgba(137, 121, 255, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                position: relative;
                overflow: hidden;
                animation: titleGlow 30s ease-in-out infinite alternate !important;
            }

            .main-title-container::before {
                content: "";
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
                animation: shimmer 2s infinite;
            }

            @keyframes titleGlow {
                0% {
                    box-shadow: 
                        0 20px 40px rgba(137, 121, 255, 0.3),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                }
                100% {
                    box-shadow: 
                        0 25px 50px rgba(137, 121, 255, 0.5),
                        0 0 0 1px rgba(255, 255, 255, 0.2) inset;
                }
            }

            @keyframes shimmer {
                0% {
                    left: -100%;
                }
                100% {
                    left: 100%;
                }
            }

            .main-title {
                font-size: clamp(1rem, 5vw, 3rem) !important;
                font-weight: 700 !important;
                color: white !important;
                text-align: center !important;
                margin: 0 !important;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                position: relative;
                z-index: 1;
            }

            /* Page subtitle styling - different colors per page */
            .page-subtitle-container {
                border-radius: 0 0 15px 15px;
                padding: 0rem;
                margin: 0 0 2rem 0;
                border-top: 3px solid #8979FF;
                box-shadow: 
                    0 10px 25px rgba(0, 0, 0, 0.2),
                    0 0 0 1px rgba(137, 121, 255, 0.1) inset;
                position: relative;
            }

            .page-subtitle {
                font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
                font-weight: 600 !important;
                color: white !important;
                text-align: center !important;
                margin: 0 !important;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            }

            /* Enhanced metrics container with uniform height and shadows */
            .metrics-row {
                display: flex;
                gap: 1rem;
                margin-bottom: 2rem;
            }

            .metric-card {
                flex: 1;
                min-height: 120px;
                background: linear-gradient(135deg, #2d2d44 0%, #3d3d5c 100%);
                border-radius: 15px;
                padding: 1.5rem 1rem;
                border: 1px solid rgba(137, 121, 255, 0.3);
                box-shadow: 
                    0 15px 35px rgba(0, 0, 0, 0.2),
                    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
                animation: cardFloat 6s ease-in-out infinite;
            }

            .metric-card:nth-child(1) { animation-delay: 0s; }
            .metric-card:nth-child(2) { animation-delay: 1.5s; }
            .metric-card:nth-child(3) { animation-delay: 3s; }
            .metric-card:nth-child(4) { animation-delay: 4.5s; }

            @keyframes cardFloat {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-5px);
                }
            }

            .metric-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #8979FF, #a855f7, #c084fc);
                opacity: 0.8;
            }

            .metric-card:hover {
                transform: translateY(-8px);
                box-shadow: 
                    0 25px 50px rgba(137, 121, 255, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                border-color: rgba(137, 121, 255, 0.6);
            }

            .stSidebar .block-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: clamp(10px, 2vw, 15px);
                padding: 0 clamp(5px, 1vw, 10px);
                position: relative;
                z-index: 1;
            }

            .stSidebar .stButton > button {
                width: 100% !important;
                max-width: 200px !important;
                min-width: 120px !important;
                height: clamp(35px, 5vh, 45px) !important;
                background: linear-gradient(135deg, #262730 0%, #2d2d44 100%) !important;
                border: 2px solid #8979FF !important;
                border-radius: 12px !important;
                font-size: clamp(12px, 2vw, 16px) !important;
                font-weight: 600 !important;
                text-align: center !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                color: white !important;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5) !important;
                position: relative !important;
                z-index: 1 !important;
            }

            .stSidebar .stButton > button::before {
                content: "";
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                transition: left 0.5s ease;
            }

            .stSidebar .stButton > button:hover {
                background: linear-gradient(135deg, #8979FF 0%, #a855f7 100%) !important;
                border-color: #c084fc !important;
                color: white !important; 
                transform: translateY(-3px) scale(1.02) !important;
                box-shadow: 
                    0 10px 25px rgba(137, 121, 255, 0.4),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
            }

            .stSidebar .stButton > button:hover::before {
                left: 100%;
            }

            .stSidebar .stButton > button:focus {
                outline: none !important;
                box-shadow: 0 0 0 3px rgba(137, 121, 255, 0.5) !important;
            }

            .stSidebar h2, .stSidebar h3 {
                text-align: center;
                margin-bottom: clamp(10px, 3vh, 20px);
                font-size: clamp(16px, 3vw, 20px) !important;
                color: white !important;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
                position: relative;
                z-index: 1;
            }
                
            .white-icon {
                color: white !important;
                filter: brightness(0) invert(1);
                font-size: clamp(12px, 2vw, 16px) !important;
            }

            .metric-container {
                background: linear-gradient(135deg, #2d2d44 0%, #3d3d5c 100%);
                padding: clamp(12px, 2vw, 20px);
                margin: 0;
                border-radius: 15px;
                border: 1px solid rgba(137, 121, 255, 0.3);
                box-shadow: 
                    0 10px 25px rgba(0, 0, 0, 0.2),
                    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
                transition: all 0.3s ease;
                position: relative;
                overflow: visible; /* CHANGED: Allow tooltip to show outside */
                min-height: 130px; /* FIXED: Uniform height for all metric cards */
                height: 130px; /* FIXED: Force same height */
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .metric-container::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, #8979FF, #a855f7, #c084fc);
                opacity: 0.8;
            }

            .metric-container:hover {
                transform: translateY(-5px);
                background: linear-gradient(135deg, #3d3d5c 0%, #4d4d6c 100%);
                box-shadow: 
                    0 20px 40px rgba(137, 121, 255, 0.3),
                    0 0 0 1px rgba(255, 255, 255, 0.1) inset;
                border-color: rgba(137, 121, 255, 0.6);
            }
            
            .metric-title {
                display: flex;
                align-items: center;
                gap: clamp(4px, 1vw, 8px);
                font-size: clamp(11px, 2vw, 14px);
                color: white;
                margin-bottom: clamp(4px, 0.5vw, 8px);
                flex-wrap: wrap;
                font-weight: 500;
                flex-shrink: 0; /* FIXED: Prevent title from shrinking */
            }
            
            .metric-value {
                font-size: clamp(20px, 6vw, 36px);
                font-weight: 700;
                color: white;
                line-height: 1.2;
                margin: 0;
                word-break: break-word;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
                flex-grow: 1; /* FIXED: Allow value to take remaining space */
                display: flex;
                align-items: center;
            }
            
            .metric-delta {
                font-size: clamp(10px, 2vw, 14px);
                color: #00d4aa;
                margin-top: clamp(4px, 0.5vw, 8px);
                display: flex;
                align-items: center;
                gap: clamp(2px, 0.5vw, 4px);
                flex-wrap: wrap;
                font-weight: 500;
                flex-shrink: 0; /* FIXED: Prevent delta from shrinking */
                min-height: 20px; /* FIXED: Reserve space even when empty */
            }
            
            .metric-delta-arrow {
                color: #00d4aa;
                font-size: clamp(8px, 1.5vw, 12px);
            }

            .tooltip {
                position: relative;
                display: inline-block;
                cursor: help;
            }

            .tooltip-icon {
                color: transparent !important;
                border: 2px solid #8979FF;
                border-radius: 50%;
                width: clamp(14px, 2vw, 18px);
                height: clamp(14px, 2vw, 18px);
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: clamp(8px, 1.5vw, 10px);
                transition: all 0.3s ease;
                background: linear-gradient(135deg, #8979FF, #a855f7);
            }

            .tooltip-icon::before {
                content: "?";
                color: white;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }

            .tooltip:hover .tooltip-icon {
                border-color: #c084fc;
                transform: scale(1.1);
                box-shadow: 0 0 10px rgba(137, 121, 255, 0.5);
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                width: clamp(150px, 30vw, 250px);
                background: linear-gradient(135deg, #2d2d44, #3d3d5c);
                color: white;
                text-align: center;
                border-radius: 8px;
                padding: clamp(8px, 1vw, 12px);
                position: absolute;
                z-index: 9999; /* FIXED: Much higher z-index */
                bottom: 150%; /* FIXED: Position above the tooltip icon */
                left: 50%;
                transform: translateX(-50%);
                opacity: 0;
                transition: all 0.3s ease;
                font-size: clamp(10px, 2vw, 12px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.4);
                border: 1px solid rgba(137, 121, 255, 0.3);
                pointer-events: none; /* FIXED: Prevent tooltip from interfering */
            }

            .tooltip .tooltiptext::after {
                content: "";
                position: absolute;
                top: 100%;
                left: 50%;
                margin-left: -5px;
                border-width: 5px;
                border-style: solid;
                border-color: #2d2d44 transparent transparent transparent;
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
                transform: translateX(-50%) translateY(-10px); /* FIXED: Move up more on hover */
            }

            .stColumns {
                gap: clamp(0.5rem, 2vw, 1rem) !important;
            }

            .js-plotly-plot {
                width: 100% !important;
                height: auto !important;
            }

            @media (max-width: 768px) {
                [data-testid="stSidebar"] {
                    width: 100% !important;
                    position: fixed !important;
                    top: 0 !important;
                    left: -100% !important;
                    height: 100vh !important;
                    z-index: 999 !important;
                    background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%) !important;
                    transition: left 0.3s ease !important;
                }

                [data-testid="stSidebar"].open {
                    left: 0 !important;
                }

                .main .block-container {
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                }

                [data-testid="collapsedControl"] ~ .main .block-container {
                    padding-left: 1rem !important;
                    padding-right: 1rem !important;
                    margin-left: auto !important;
                    margin-right: auto !important;
                    max-width: 100% !important;
                }

                .main-title-container {
                    padding: 1.5rem 1rem;
                    margin: 0 0 0.25rem 0;
                }

                .page-subtitle-container {
                    padding: 0.75rem;
                    margin: 0 0 1.5rem 0;
                }

                .metric-card {
                    min-height: 100px;
                    padding: 1rem 0.75rem;
                }

                .stSidebar .stButton > button {
                    width: 90% !important;
                    margin: 0 auto !important;
                    font-size: 14px !important;
                    height: 40px !important;
                }

                .metric-container {
                    text-align: center;
                    padding: 12px 8px;
                    min-height: 110px; /* FIXED: Adjusted for mobile */
                    height: 110px;
                }

                .metric-title {
                    justify-content: center;
                    text-align: center;
                }

                .metric-value {
                    font-size: clamp(18px, 8vw, 28px);
                }

                /* Stack columns on mobile */
                .stColumns > div {
                    width: 100% !important;
                    margin-bottom: 1rem;
                }
            }

            @media (max-width: 480px) {
                .main-title {
                    font-size: clamp(1.4rem, 6vw, 2.2rem) !important;
                }

                .page-subtitle {
                    font-size: clamp(1rem, 4vw, 1.4rem) !important;
                }

                .metric-title {
                    font-size: 11px;
                    gap: 4px;
                }

                .metric-value {
                    font-size: clamp(16px, 10vw, 24px);
                }

                .metric-delta {
                    font-size: 10px;
                }

                .tooltip .tooltiptext {
                    width: 120px;
                    font-size: 10px;
                    padding: 6px;
                }

                .metric-container {
                    min-height: 100px;
                    height: 100px;
                }
            }

            @media (min-width: 769px) and (max-width: 1024px) {
                [data-testid="stSidebar"] {
                    width: clamp(160px, 18vw, 200px) !important;
                }

                .metric-value {
                    font-size: clamp(24px, 5vw, 32px);
                }

                [data-testid="collapsedControl"] ~ .main .block-container {
                    padding-left: clamp(3rem, 6vw, 5rem) !important;
                    padding-right: clamp(3rem, 6vw, 5rem) !important;
                }

                .metric-container {
                    min-height: 120px;
                    height: 120px;
                }
            }

            @media (min-width: 1200px) {
                [data-testid="stSidebar"] {
                    width: 250px !important;
                }

                .metric-container {
                    padding: 24px 20px;
                    min-height: 140px;
                    height: 140px;
                }

                .metric-value {
                    font-size: 36px;
                }

                [data-testid="collapsedControl"] ~ .main .block-container {
                    padding-left: clamp(4rem, 10vw, 8rem) !important;
                    padding-right: clamp(4rem, 10vw, 8rem) !important;
                    max-width: 1400px !important;
                }
            }

            /* Print styles */
            @media print {
                [data-testid="stSidebar"] {
                    display: none !important;
                }

                .metric-container, .metric-card {
                    break-inside: avoid;
                }
            }

            /* High contrast mode support */
            @media (prefers-contrast: high) {
                .metric-container, .metric-card {
                    border: 2px solid white;
                }

                .tooltip-icon {
                    border-width: 2px;
                }
            }

            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                .stSidebar .stButton > button,
                .metric-container,
                .metric-card,
                .tooltip .tooltiptext,
                .main-title-container,
                .page-subtitle-container {
                    animation: none !important;
                    transition: none !important;
                }

                .stSidebar .stButton > button:hover,
                .metric-container:hover,
                .metric-card:hover {
                    transform: none !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)