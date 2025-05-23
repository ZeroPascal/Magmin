
import { Button, Collapse, IconButton, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from "@mui/material"

import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import React, { useState } from "react"
import { useSelector } from "react-redux"
import { getFolders } from "../../../app/Folders/foldersSelector"
import { Folder } from "../../../app/Folders/foldersSlice"
import { deleteDirectory, scanDirectory } from "../../../app/Socket/socketSenders"
import { RootState } from "../../../app/store"
import { getFilesFromFolder } from "../../../app/Files/filesSelectors";

import FileList from "./FileList";
import { red } from "@mui/material/colors";

function FoldersListRow(props:{folder:Folder}){
    const [open,setOpen]=useState(false)
    const state = useSelector((state: RootState) => state)
    const {folder} =props

    return (
        <React.Fragment key={'folderListRow_frag'+folder.name}>
            <TableRow key={'folderListRow'+folder.name} sx={{ '& > *': { borderBottom: 'unset' } }}>
            <TableCell key={'folderListRow_open'+folder.name}>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
          </TableCell>
                <TableCell key={'folderListRow_name'+folder.name}>{folder.name}</TableCell>
                <TableCell key={'folderListRow_path'+folder.name}>{folder.root}</TableCell>
                <TableCell key={'folderListRow_rec'+folder.name}>{folder.recursive?'True':'False'}</TableCell>
                <TableCell key={'folderListRow_lastScan'+folder.name}>{folder.lastScan}</TableCell>
                <TableCell key={'folderListRow_scan'+folder.name}><Button variant="outlined"  key={'folderListRow_scanB'+folder.name} onClick={(e)=>scanDirectory(folder.name)}>Scan</Button></TableCell>
                <TableCell key={'folderListRow_delete'+folder.name}><Button variant="outlined"  key={'folderListRow_deleteB'+folder.name} onClick={(e)=>deleteDirectory(folder.name)}>Delete</Button></TableCell>
            </TableRow>
            <TableRow>
        <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
          <Collapse in={open} timeout="auto" unmountOnExit>
           <FileList files={getFilesFromFolder(state,folder.root)}/>
            </Collapse>
            </TableCell>
            </TableRow>
        </React.Fragment>
    )

}
function FoldersList(){
    const state = useSelector((state: RootState) => state)

    const folderList=()=>{
        return getFolders(state).map(folder=>{
            return <FoldersListRow key={'folderListRow'+folder.name}folder={folder}/>
            
        })
    }
    return(
        <div key='FoldersList'>
            <Typography fontSize={25} align='left'>Existing Folders</Typography>
           <TableContainer  component={Paper}>
            <Table key='folderList_table'>
                <TableHead key='folderlist_tablehead'>
                    <TableCell/>
                    <TableCell key='folderList_headerName'>Name</TableCell>
                    <TableCell key='folderlist_headerPath'>Path</TableCell>
                    <TableCell key='folderlist_headerRec'>Recursive</TableCell>
                    <TableCell key='folderlist_headerLastScan'>Last Scanned</TableCell>
                    <TableCell key='folderlist_headerScan'>Scan</TableCell>
                    <TableCell key='folderlist_headerDelete'>Delete</TableCell>
                </TableHead>
                <TableBody key='folderlist_body'>
                {folderList()}
                </TableBody>
            </Table>
            </TableContainer>
           
        </div>
    )
}

export default FoldersList