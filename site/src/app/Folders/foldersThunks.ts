import { createAsyncThunk } from "@reduxjs/toolkit";
import { addDirectory } from "./folderAPI";
import { Folder } from "./foldersSlice";

export const addDirectoryThunk = createAsyncThunk(
    'folder/addFolder',
    async ()=>{
        console.log('Thunking')
        const f:Folder={
            root: 'root',
            name: 'path',
            recursive: false,
            lastScan: 0
        }
        const response =await addDirectory(f);
        console.log(response)
        return response

    }
)