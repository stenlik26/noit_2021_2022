export class UserInfo{
    username: string = '';
    picture: string = '';
    object_id: string = '';

    constructor(user_json: any)
    {
        this.username = user_json.name;
        if(user_json.picture != ""){
            this.picture = user_json.picture;
        }
        else{
            this.picture = '../assets/icons/user.png';
        }
        this.object_id = user_json._id;
    }

    get_username(): string{
        return this.username;
    }

    get_picture(): string{
        return this.picture;
    }

    get_user_id(): string{
        return this.object_id;
    }
}