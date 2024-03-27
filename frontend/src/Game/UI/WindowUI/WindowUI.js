import Moveable from 'react-moveable'
import { useRef, cloneElement, Children} from 'react'


const WindowUI = ({canDrag=true, canResize=true, children}) => {
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
        draggable={canDrag}
        scalable={canResize}
        keepRatio={true}
        throttleDrag={0}
        container={null}
        origin={true}
        onDragStart={({inputEvent}) => {
            return !(inputEvent.detail == 2)
        }}
        onDrag={({target, transform}) => {
            target.style.transform = transform
        }}
        onScale={({target, transform}) => {
                target.style.transform = transform;
            }}/>
        </>
    )
}
export default WindowUI