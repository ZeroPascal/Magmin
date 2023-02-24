import { Box, Button, TextField, Typography } from "@mui/material"
import { useState } from "react"
import { addDirectory } from "../../../app/Socket/socketSenders"

function AddFolder(){
    const [root,setRoot]=useState('')
    const [name,setName]=useState('')
    const [recursive,setRecursive]=useState(false)

    const handleSubmit=()=>{
        addDirectory(root,name,recursive)
        setRoot('')
        setName('')
        setRecursive(false)
    }

    return(
        <div key='addFolder_Div' >
           <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            Add Folder
                        </Typography >
            <TextField size='small'sx={{padding:1, height:'2px'}}key='addFolder_name'type={'text'} label='Name' value={name} onChange={(e)=>setName(e.target.value)}/>
            <TextField size='small'sx={{padding:1}}key='addFolder_root'type={'text'} label='Path' value={root} onChange={(e)=>setRoot(e.target.value)}/>

            <label key='addFolder_recLabel' htmlFor={"addFolder_recursive"}>Recursive</label>
            <input key='addFolder_recursive'type={'radio'} checked={recursive} onChange={(e)=>setRecursive(!recursive)}></input>
       
            <Button size='small'  variant='contained'  onClick={()=>handleSubmit()}>Add Folder</Button>
        </div>
    )
}

export default AddFolder