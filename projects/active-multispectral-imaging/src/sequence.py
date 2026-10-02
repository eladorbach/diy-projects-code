"""Band sequencer for active multispectral capture.

Supply a capture callback that accepts (channel, output_path). Camera setup should
normally happen once outside the per-band loop.
"""

from pathlib import Path
import time

from led_controller import LedController


def capture_bands(
    capture_frame,
    output_dir,
    pwm_counts,
    channels=None,
    settle_seconds=0.05,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    channels = list(range(len(pwm_counts))) if channels is None else list(channels)
    if len(channels) != len(pwm_counts):
        raise ValueError("channels and pwm_counts must have the same length")

    with LedController() as leds:
        for index, (channel, duty) in enumerate(zip(channels, pwm_counts), start=1):
            leds.all_off()
            leds.set_output(channel, duty)
            time.sleep(settle_seconds)

            path = output_dir / f"band_{index:02d}_channel_{channel:02d}.png"
            capture_frame(channel, path)

        leds.all_off()


if __name__ == "__main__":
    raise SystemExit(
        "Import capture_bands() and provide a camera-specific capture_frame callback."
    )
