declare namespace React {
  interface ReactNode {}
  interface Component<P = {}, S = {}> {}
  interface FC<P = {}> {
    (props: P): ReactNode
  }
  interface KeyboardEvent<T = Element> {
    key: string
    shiftKey: boolean
    preventDefault(): void
  }
  interface MouseEvent<T = Element> {
    preventDefault(): void
  }
  interface ChangeEvent<T = Element> {
    target: T & { value: string }
  }
}

declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any
  }
}

declare module 'react' {
  const useState: <T>(initial: T) => [T, (value: T | ((prev: T) => T)) => void]
  const useEffect: (effect: () => void | (() => void), deps?: any[]) => void
  const useRef: <T>(initial: T | null) => { current: T | null }
  const useCallback: <T extends (...args: any[]) => any>(callback: T, deps: any[]) => T
  const useMemo: <T>(factory: () => T, deps: any[]) => T
  const Component: any
  const ReactNode: any
  export { useState, useEffect, useRef, useCallback, useMemo }
  export = React
  export as namespace React
}

declare module 'react-dom' {
  export = ReactDOM
}

declare module 'next/link' {
  interface LinkProps {
    href: string
    children: React.ReactNode
    className?: string
  }
  const Link: React.FC<LinkProps>
  export default Link
}

declare module 'next/navigation' {
  export function useRouter(): {
    push: (url: string) => void
    back: () => void
    forward: () => void
  }
}

declare module 'framer-motion' {
  interface MotionProps {
    initial?: any
    animate?: any
    exit?: any
    transition?: any
    variants?: any
    whileHover?: any
    whileTap?: any
    onHoverStart?: () => void
    onHoverEnd?: () => void
    onClick?: () => void
    onKeyDown?: (e: any) => void
    className?: string
    children?: React.ReactNode
    style?: any
    tabIndex?: number
    role?: string
    'aria-label'?: string
    'aria-expanded'?: boolean
    disabled?: boolean
    [key: string]: any
  }
  
  export const motion: {
    div: React.FC<MotionProps>
    button: React.FC<MotionProps>
    h1: React.FC<MotionProps>
    h2: React.FC<MotionProps>
    h3: React.FC<MotionProps>
    p: React.FC<MotionProps>
    span: React.FC<MotionProps>
    svg: React.FC<MotionProps>
    circle: React.FC<MotionProps>
    path: React.FC<MotionProps>
    text: React.FC<MotionProps>
    g: React.FC<MotionProps>
    a: React.FC<MotionProps>
    [key: string]: React.FC<MotionProps>
  }
  
  export const AnimatePresence: React.FC<{ children?: React.ReactNode }>
}

declare module 'clsx' {
  function clsx(...args: any[]): string
  export { clsx }
}