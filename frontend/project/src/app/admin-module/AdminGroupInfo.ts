export class AdminGroupInfo
{
    group_id: string = '';
    ammount_of_users: string = '';
    group_title: string = '';

    constructor(json_data: any){
        this.group_id = json_data._id.$oid;
        this.ammount_of_users = json_data.users;
        this.group_title = json_data.name;
    }
}