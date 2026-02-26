# Physics Simulation Engine (Python + PyQt)

A real-time 2D physics simulator built in Python using PyQt.  
This project models gravity-driven motion with boundary collision handling and interactive parameter controls.

---

## Overview

This simulator renders a ball undergoing gravity-based motion within a bounded environment. Users can dynamically adjust physical parameters such as gravity, velocity, and object size to observe real-time behavioral changes.

The project emphasizes modular architecture, event-driven UI integration, and real-time simulation updates.

---

## Features

- Real-time 2D physics simulation
- Gravity-driven projectile motion
- Ground collision response
- Adjustable simulation parameters:
  - Gravity
  - Initial velocity
  - Ball size
- Event-driven user interaction
- Modular code structure separating:
  - Simulation logic
  - Rendering
  - UI controls

---

## Tech Stack

- **Language:** Python  
- **Framework:** PyQt (Qt for Python)

---

## Project Structure

main.py # Application entry point
simulator.py # Physics and simulation logic
options.py # Adjustable simulation parameters
landing.py # UI initialization / layout

---

## How It Works

The simulation updates object position using time-stepped motion equations.  
When the ball collides with the ground boundary, velocity is reflected to simulate bounce behavior.

The rendering loop integrates PyQt’s event system to maintain smooth frame updates while allowing real-time parameter adjustments.

---

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/physics-simulator.git
cd physics-simulator

pip install PyQt5

python main.py
