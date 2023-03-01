import { Dispatch } from "react";
import { Socket } from "socket.io-client";
import { setFiles } from "../Files/filesSlice";
import { setFolders } from "../Folders/foldersSlice";
import { socketCommands } from "./socketCommands";

export default function socketListeners(socket: Socket, d: Dispatch<any>){
    socket.onAny((event,payload)=>{
        console.log(socket.id)
        console.log(event,payload)
        switch(event){
            case socketCommands.SENDING_FOLDERS:
                d(setFolders(payload))
                break;
            case socketCommands.SENDING_FILES:
                if(payload){
                    d(setFiles(payload))
                }
               
                break;
         
        }
    })

}
