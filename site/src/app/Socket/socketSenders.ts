
import { Folder } from "../Folders/foldersSlice";
import { socket } from "./Socket";
import { socketCommands } from "./socketCommands";

export function addDirectory(root:string,name:string,recursive:boolean){
    const f:Folder={
        root,name,recursive,lastScan:0
    }
    socket.emit(socketCommands.ADD_DIRECTORY,f)
}

export function deleteDirectory(name:string){
    socket.emit(socketCommands.REMOVE_DIRECTORY,name)
}

export function scanDirectory(name:string){
    socket.emit(socketCommands.SCAN_DIRECTORY,name)
}