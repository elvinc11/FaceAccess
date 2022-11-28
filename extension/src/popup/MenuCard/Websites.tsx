import React, { useEffect, useState} from 'react';
import Typography from '@mui/material/Typography';
import { fetchBlockedWebsites, WebsiteData } from '../../utils/api';
import { setStoredUrls, getStoredUrls } from '../../utils/storage';


export default function Websites(){
    const [website, setWebsite] = useState<WebsiteData[]|null>(null)
    const [isLoading, setLoading] = useState(true);
    const [url, setUrl] = useState([]);
    const urls = []
    useEffect(()=>{
      fetchBlockedWebsites().then(data =>{
        setWebsite(data);
        if(data == null){
          setLoading(true);
        } else {
          setLoading(false);
        }  
      }).catch(error =>{
        console.log(error)
      })
    },[]);
   
    return (
        <Typography component={'span'} variant="body2">
        {!isLoading ? website.map((web)=>{
           urls.push(web.url);
          setStoredUrls(urls);
            return(
              <div key={web.website_id.toString()}>
                {web.url}
              </div>
            )
        } ) : <div>No hay sitios web bloqueados</div>}
        </Typography> 
    );
}
    



