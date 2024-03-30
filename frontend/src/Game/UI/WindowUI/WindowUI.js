import Moveable from 'react-moveable'
import { useRef, cloneElement, Children} from 'react'


const WindowUI = ({draggable=true, scalable=true, resizable=false, children}) => {
    const childrenRef = useRef([])
    return (
        <>
        {Children.map(children, (child, index) =>
        cloneElement(child, {
          ref: (ref) => (childrenRef.current[index] = ref)
        })
        )}
        <Moveable 
        hideDefaultLines={true}
        target={childrenRef}
        edge={false}
        draggable={draggable}
        scalable={scalable}
        resizable={resizable}
        keepRatio={true}
        throttleDrag={0}
        container={null}
        origin={true}
        
        onDragStart={({inputEvent}) => {
            return inputEvent.detail === 2
        }}
        onDrag={({target, transform, inputEvent}) => {
            target.style.transform = transform
        }}
        onScale={({target, transform}) => {
                target.style.transform = transform;
            }}
        onResize={({target, delta, width, height}) => {
            delta[0] && (target.style.width = `${width}px`);
            delta[1] && (target.style.height = `${height}px`);
        }}    
        />
        </>
    )
}
export default WindowUI