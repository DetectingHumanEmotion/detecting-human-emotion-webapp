try:
    from deception_detection.audio.paura2 import run_audio_deception_stream
    from deception_detection.visual.detect_multi_threaded import record
except ModuleNotFoundError:
    from .deception_detection.audio.paura2 import run_audio_deception_stream
    from .deception_detection.visual.detect_multi_threaded import record
