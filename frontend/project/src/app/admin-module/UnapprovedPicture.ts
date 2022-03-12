import projectConfig from '../../assets/conf.json';

export class UnapprovedPicture {
    user_id = '';
    userName = '';
    path_full = '';
    time = '';
    id = '';

    constructor(pic_id:string, user_id: string, user_name: string, pic_path: string, time: string)
    {
        this.id = pic_id;
        this.user_id = user_id;
        this.userName = user_name;
        this.path_full = projectConfig.picture_url + pic_path;
        this.time = time;
    }

    getTime(): string{
        return this.time;
    }

    getUserId(): string{
        return this.user_id;
    }

    getUserName(): string{
        return this.userName;
    }

    getPicPath(): string{
        return this.path_full;
    }

    getId(): string{
        return this.id;
    }
}
