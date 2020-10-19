##! File Upload attack detection.

@load base/protocols/http/main.zeek
@load base/frameworks/notice
export {
    redef enum Notice::Type += {
        File_Upload,
    };
}
event http_entity_data(c: connection, is_orig: bool, length: count, data: string)
    {
   
    print(data);
    #"/bl-content/uploads/pages" in c$http$uri ||
        if ( "/bl-content/uploads/pages" in c$http$uri || "eval" in data || "fsockopen" in data )
            {
            print(c$http$uri);
            local n: Notice::Info = Notice::Info($note=File_Upload, 
                                                 $msg="bludit 3.9.2 File Upload attack", 
                                                 $sub=data,
                                                 $conn=c);
            NOTICE(n);
            }
    }
