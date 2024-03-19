import Draggable from 'react-draggable'


function Settings(props) {
    return (
        <>
        { props.viewSettings &&
            <Draggable>
            <div className="fixed right-0 z-20 bg-gray-900">
                Settings Window
            </div>
            </Draggable>
        }
        </>
    )
}
export default Settings