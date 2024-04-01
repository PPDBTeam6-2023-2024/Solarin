import WindowUI from "../WindowUI/WindowUI"

function Settings(props) {
    return (
        <>
        { props.viewSettings &&
            <WindowUI>
            <div className="fixed right-0 z-20 bg-gray-900">
                Settings Window
            </div>
            </WindowUI>
        }
        </>
    )
}
export default Settings