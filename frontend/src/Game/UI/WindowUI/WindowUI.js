import Moveable from 'react-moveable'
import {useRef, cloneElement, Children, useEffect, useId, useState} from 'react'
import {useDispatch, useSelector} from 'react-redux'
import {addWindow, removeWindow} from '../../../redux/slices/hiddenWindowsSlice'


const WindowUI = ({draggable = true, scalable = true, resizable = false, hideState, windowName = null, children}) => {
    const childrenRef = useRef([])

    const dispatch = useDispatch()
    const hiddenWindows = useSelector((state) => state.hiddenWindows.windows)

    const id = useId()

    const window = windowName || id

    useEffect(() => {
        if (hideState) dispatch(addWindow(window))
        else dispatch(removeWindow(window))
    }, [hideState])

    return (hiddenWindows.indexOf(window) === -1 &&
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
                onDrag={({target, transform}) => {
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