import {TreeView, TreeItem} from '@mui/x-tree-view'
import WindowUI from '../WindowUI/WindowUI'
function MilitaryViewer(props) {
  // TODO: with more info (ap, dp, cap, cdp, ...) and more icons, ...
    const example_armies_input = [
      {'name': 'Red Dragon',
        'general': {'name': 'Tarkin'},
        'troops': [
           {'type': 'Assassin', "count": 10},
           {'type': 'Tank', "count": 3}
        ]
      },
      {'troops': [
          {'type': 'Tank', "count": 6}
      ]},
      {'name': "Hawk's Fist",
        'troops': [
          {'type': 'Soldier', "count": 2}
        ]
      }
    ]
    let example_armies_output = []
    example_armies_input.forEach((elem, index) => {
      const name_str = (elem.name) ? `'${elem.name}'` : ""
      let troops_output = []
      elem.troops.forEach((elem, sub_index) => {
          troops_output.push(<TreeItem nodeId={`${index}-${sub_index}`} label={`${elem.count}x Troop ${elem.type}`}/>)
      })
      example_armies_output.push(
      <TreeItem className="border-2" sx={{padding: "0.25rem"}} nodeId={`${index}`} label={`Army ${index} ${name_str}`}>
        {troops_output}
        </TreeItem>)
    })
    return (
      <WindowUI>
        <TreeView
        className="bg-gray-600 fixed border-4"
      aria-label="file system navigator"
      sx={{zIndex: 1, flexGrow: 1, overflowY: 'auto', padding: "1rem"}}
      >
      <h1 className="text-2xl my-1">Armies</h1>
      {example_armies_output}
    </TreeView>
    </WindowUI>
    )
}
export default MilitaryViewer;