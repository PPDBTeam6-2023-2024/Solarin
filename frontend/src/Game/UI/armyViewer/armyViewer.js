import {TreeView, TreeItem} from '@mui/x-tree-view'
import Draggable from 'react-draggable'

function ArmyViewer(props) {
    // TODO: with more info (ap, dp, cap, cdp, ...) and more icons, ...
    const example_armies_input = [
        {
            'name': 'Red Dragon',
            'general': {'name': 'Tarkin'},
            'troops': [
                {'type': 'Assassin', "count": 10},
                {'type': 'Tank', "count": 3}
            ]
        }
    ]
    let example_armies_output = []
    let elem = example_armies_input[0]
    let index = 0
    const name_str = (elem.name) ? `'${elem.name}'` : ""
    let troops_output = []
    let totalcount = 0
    elem.troops.forEach((elem, sub_index) => {
        troops_output.push(<TreeItem nodeId={`${index}-${sub_index}`} label={`${elem.count}x Troop ${elem.type}`}/>)
        totalcount += elem.count
    })

    example_armies_output.push(
        <TreeItem className="border-2" sx={{padding: "0.25rem"}} nodeId={`${index}`}
                  label={`stats`}>
        </TreeItem>)
    example_armies_output.push(
        <TreeItem className="border-2" sx={{padding: "0.25rem"}} nodeId={`${index}`}
                  label={` ${totalcount} troops`}>
            {troops_output}
        </TreeItem>)


    return (
        <Draggable>
            <TreeView
                className="bg-gray-600 fixed border-4"
                aria-label="file system navigator"
                sx={{zIndex: 1, flexGrow: 1, overflowY: 'auto', padding: "1rem"}}
            >
                <h1 className="text-2xl my-1">Army 1</h1>
                {example_armies_output}
            </TreeView>
        </Draggable>
    )
}

export default ArmyViewer;