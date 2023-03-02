import { Backdrop, Box, Button, Card, Checkbox, Paper, TextField, Typography } from "@mui/material"
import { useState } from "react"
import { addDirectory } from "../../../app/Socket/socketSenders"

function AddFolder(){
    const [root,setRoot]=useState('')
    const [name,setName]=useState('')
    const [recursive,setRecursive]=useState(false)
    const [backdropOpen,setBackdropOpen]=useState(false)

    const handleSubmit=()=>{
        addDirectory(root,name,recursive)
        setRoot('')
        setName('')
        setRecursive(false)
        setBackdropOpen(false)
    }
    const handleCancel=()=>{
        setBackdropOpen(false)
    }


    return(
        <div key='addFolder_Div' >
              <Backdrop open={backdropOpen} >
                <Paper sx={{width:'50%', height:'40%', minHeight:300}}>
                <br></br>
           <Typography variant="h6" component="div">
                            Add Folder
                        </Typography >
            <TextField size='small'key='addFolder_name'type={'text'} label='Name' value={name} onChange={(e)=>setName(e.target.value)}/>
            <br></br>
            <TextField size='small'key='addFolder_root'type={'text'} label='Path' value={root} onChange={(e)=>setRoot(e.target.value)}/>
            <br></br>
            <label key='addFolder_recLabel' htmlFor={"addFolder_recursive"}>Recursive</label>
            <Checkbox key='addFolder_recursive' checked={recursive} onChange={(e)=>setRecursive(!recursive)}></Checkbox>
            <br></br>
            <Button size='small'  variant='contained'  onClick={()=>handleSubmit()}>Add Folder</Button>
            <br></br>
            <br></br>
            <Button size='small'   onClick={()=>handleCancel()}>Cancle</Button>
            </Paper>
        </Backdrop>
            {backdropOpen?undefined:<Button size='small'  variant='contained'  onClick={()=>setBackdropOpen(!backdropOpen)}>Add Folder</Button>}
        </div>
    )
}

export default AddFolder