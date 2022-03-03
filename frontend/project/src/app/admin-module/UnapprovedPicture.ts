export class UnapprovedPicture {
    user_id = '';
    userName = '';
    path_full = '';
    time = '';
    id = '';

    constructor(user_id: string, user_name: string, pic_path: string, time: string)
    {
        this.user_id = user_id;
        this.userName = user_name;
        this.path_full = pic_path;
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
