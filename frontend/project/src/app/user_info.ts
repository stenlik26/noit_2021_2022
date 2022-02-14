export class UserInfo{
    username: string = '';
    picture: string = '';
    object_id: string = '';
    is_admin: boolean = false;
    email: string = '';

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
        if(user_json.is_admin != undefined){
            this.is_admin = user_json.is_admin;
        }
        this.email = user_json.email;
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

    get_user_is_admin(): boolean{
        return this.is_admin;
    }

    get_user_status(): string{
        return (this.is_admin ? "Администратор" : "Потребител");
    }

    get_email(): string{
        return this.email;
    }
}