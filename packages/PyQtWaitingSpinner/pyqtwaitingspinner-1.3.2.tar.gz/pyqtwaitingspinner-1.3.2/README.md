# PyQtWaitingSpinner

![Python](https://img.shields.io/badge/python-3.8_|_3.9_|_3.10_|_3.11_|_3.12_-ffff54?style=for-the-badge&logo=python&logoColor=ffdd54&labelColor=3670A0)
![Static Badge](https://img.shields.io/badge/Qt-6.7.0-0?logo=qt&logoColor=white&style=for-the-badge)
![Static Badge](https://custom-icon-badges.demolab.com/badge/license-MIT-blue?logoColor=blue&style=for-the-badge&logo=law)

![PyPI - Version](https://img.shields.io/pypi/v/pyqtwaitingspinner)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/pyqtwaitingspinner)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyqtwaitingspinner)
<!-- ![GitLab Issues](https://img.shields.io/gitlab/issues/open/Batticus%2FPyQtWaitingSpinner) -->
![GitLab Issues](https://img.shields.io/gitlab/issues/open/Batticus/pyqtwaitingspinner)

<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dd/pyqtwaitingspinner)
![PyPI - Downloads](https://img.shields.io/pypi/dw/pyqtwaitingspinner)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyqtwaitingspinner) -->

(Py)QtWaitingSpinner is a highly configurable, custom (Py)Qt widget for showing "waiting", or
"loading", spinner icons in (Py)Qt applications.

Based on [pyqtspinner](https://github.com/fbjorn/QtWaitingSpinner), by [fbjorn](https://github.com/fbjorn), which is a fork of [z3ntu](https://github.com/z3ntu/QtWaitingSpinner)'s port of [snowwlex](https://github.com/snowwlex)'s [QtWaitingSpinner](https://github.com/snowwlex/QtWaitingSpinner).

The spinners below are all (Py)QtWaitingSpinner widgets, differing only in their configuration:

<!-- <img src="static/WaitingSpinner-04.gif" width=56 height=56>
<img src="static/WaitingSpinner-02.gif" width=56 height=56>
<img src="static/WaitingSpinner-03.gif" width=56 height=56>
<img src="static/WaitingSpinner-01.gif" width=56 height=56>
<br> -->
<!-- <img src="static/waiting-spinners.gif"> -->

<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/WaitingSpinner-04.gif?ref_type=heads" width=56 height=56>
<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/WaitingSpinner-03.gif?ref_type=heads" width=56 height=56>
<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/WaitingSpinner-02.gif?ref_type=heads" width=56 height=56>
<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/WaitingSpinner-01.gif?ref_type=heads" width=56 height=56>
<br>
<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/waiting-spinners.gif?ref_type=heads">

<sup>Original GIF by [snowwlex](https://github.com/snowwlex)</sup>

<!-- <img src="static/examples.png" alt="Original GIF by snowwlex" width=504 height=415> -->
<img src="https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/examples.png?ref_type=heads" alt="Original GIF by snowwlex" width=504 height=415>

<sup>Original Image by [fbjorn](https://github.com/fbjorn)</sup>

---

# Installation

`pip install pyqtwaitingspinner`

---

# Dependencies

- [PyYAML](https://pypi.org/project/PyYAML/)
- [PyQt6](https://pypi.org/project/PyQt6/)

---

# Configuration

The following properties can all be controlled directly through their corresponding
properties:

- Color of the widget
- "Roundness" of the lines
- Speed (rotations per second)
- Number of lines to be drawn
- Line length
- Line width
- Radius of the spinner's "dead space" or inner circle
- The percentage fade of the "trail"
- The minimum opacity of the "trail"
- Whether to center the spinner on its parent widget
- Whether or not to disable the parent widget whilst the spinner is spinning
- The direction in which the spinner will spin

---

# Usage

## *Spinner*

The following code will create a simple spinner that

- (1) blocks all user input to the main application for as long as the spinner is active
- (2) automatically centers itself on its parent widget every time "start" is called
- (3) makes use of the default shape, size and color settings.

```python
spin_pars = SpinnerParameters(disable_parent_when_spinning=True)
spinner = WaitingSpinner(parent, spin_pars)
```

## *Configurator*

The graphical Configurator allows you edit the parameters of the spinner, and view the changes live.

The Configurator can be launched with:

```
spinner-conf
```

<!-- ![configuration](static/configurator.png "Configurator") -->
![configuration](https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/configurator.png?ref_type=heads "Configurator")

Once the spinner's appearance is to your liking, you can either copy (and view) the initialization parameters for the construction of a `SpinnerParameters` object, or you can save the spinner as a YAML configuration and load it from within a `WaitingSpinner` class.

### Show Init Args

Pressing the **`Show Init Args`** button will show the initialization arguments for the equivalent **`SpinnerParameters`** object, and will make a copy to the clipboard, ***including newlines and whitespace***.

<!-- ![show-init-args](static/show-init-args.png "Show Init Args") -->
![show-init-args](https://gitlab.com/Batticus/pyqtwaitingspinner/-/raw/main/static/show-init-args.png?ref_type=heads "Show Init Args")
```python
SpinnerParameters(
    roundness=100.0,
    trail_fade_percentage=67.0,
    number_of_lines=8,
    line_length=40,
    line_width=40,
    inner_radius=32,
    revolutions_per_second=1.0,
    color=QColor(0, 170, 0),
    minimum_trail_opacity=1.0,
    spin_direction=SpinDirection.COUNTERCLOCKWISE,
    center_on_parent=True,
    disable_parent_when_spinning=False,
)
```

### Save Config
Pressing the **`Save`** button will open a dialog allowing you to select the location, and name, in which to save the configured spinner. The outputted **YAML** file can then be loaded like so:

```python
spinner = WaitingSpinner(parent)
spinner.load("path/to/spinner.yaml")
```

---

# Documentation

Full documentation at [ReadTheDocs](https://pyqtwaitingspinner.readthedocs.io/en/latest/)

---

# Credits

- [snowwlex (Alex Turkin)](https://github.com/snowwlex), [William Hallatt](https://github.com/williamhallatt), & [jacob3141 (Jacob Dawid)](https://github.com/jacob3141) for the original Qt widget.
- [z3ntu (Luca Weiss)](https://github.com/z3ntu) for his [PyQt6 port](https://github.com/z3ntu/QtWaitingSpinner).
- [fbjorn](https://github.com/fbjorn) for his [PyQt5 port](https://github.com/fbjorn/QtWaitingSpinner) of [z3ntu](https://github.com/z3ntu)'s port.
- [Yusuke Kamiyamane](http://p.yusukekamiyamane.com) for the icons used in the Configurator.

- See full [credits](https://pyqtwaitingspinner.readthedocs.io/en/latest/credits/)

---

Enjoy!
