import { useCallback, useMemo } from 'react'

export interface ParticleConfig {
  background: {
    color: {
      value: string
    }
  }
  fpsLimit: number
  interactivity: {
    events: {
      onClick: {
        enable: boolean
        mode: string
      }
      onHover: {
        enable: boolean
        mode: string
      }
      resize: boolean
    }
    modes: {
      push: {
        quantity: number
      }
      repulse: {
        distance: number
        duration: number
      }
    }
  }
  particles: {
    color: {
      value: string[]
    }
    links: {
      color: string
      distance: number
      enable: boolean
      opacity: number
      width: number
    }
    collisions: {
      enable: boolean
    }
    move: {
      direction: string
      enable: boolean
      outModes: {
        default: string
      }
      random: boolean
      speed: number
      straight: boolean
    }
    number: {
      density: {
        enable: boolean
        area: number
      }
      value: number
    }
    opacity: {
      value: number
    }
    shape: {
      type: string
    }
    size: {
      value: {
        min: number
        max: number
      }
    }
  }
  detectRetina: boolean
}

export function useParticles() {
  const particleConfig: ParticleConfig = useMemo(() => ({
    background: {
      color: {
        value: 'transparent',
      },
    },
    fpsLimit: 120,
    interactivity: {
      events: {
        onClick: {
          enable: true,
          mode: 'push',
        },
        onHover: {
          enable: true,
          mode: 'repulse',
        },
        resize: true,
      },
      modes: {
        push: {
          quantity: 4,
        },
        repulse: {
          distance: 200,
          duration: 0.4,
        },
      },
    },
    particles: {
      color: {
        value: ['#007FFF', '#66B2FF', '#00E5FF'],
      },
      links: {
        color: '#66B2FF',
        distance: 150,
        enable: true,
        opacity: 0.2,
        width: 1,
      },
      collisions: {
        enable: false,
      },
      move: {
        direction: 'none',
        enable: true,
        outModes: {
          default: 'bounce',
        },
        random: false,
        speed: 1,
        straight: false,
      },
      number: {
        density: {
          enable: true,
          area: 800,
        },
        value: 80,
      },
      opacity: {
        value: 0.5,
      },
      shape: {
        type: 'circle',
      },
      size: {
        value: { min: 1, max: 3 },
      },
    },
    detectRetina: true,
  }), [])

  const particlesInit = useCallback(async (engine: any) => {
    // This loads the tsparticles package bundle, it's the easiest method for getting everything ready
    await import('@tsparticles/slim').then(({ loadSlim }) => loadSlim(engine))
  }, [])

  const particlesLoaded = useCallback(async (container: any) => {
    // Optional callback for when particles are loaded
  }, [])

  return {
    particleConfig,
    particlesInit,
    particlesLoaded,
  }
}