export class ProblemInformationPick{
    difficulty = '';
    title ='';
    tags: Array<String> = new Array<String>();
    num: number = 0;
    object_id: string = '';

    parse_difficulty(diff: string): string{
        switch(diff){
            case 'easy':
                return 'Лесна';
            case 'medium':
                return 'Средна';
            case 'hard':
                return 'Трудна';
            case '-':
                return '';
            default:
                return 'Възникна грешка!';
        }
    }

    get_tags(): string{
        return this.tags.join(", ").toString();
    }

    constructor(num: number,  title: string, difficulty: string, tags: Array<any>, id: string)
    {
        this.difficulty = this.parse_difficulty(difficulty);
        this.title = title;
        this.tags = tags;
        this.num = num;
        this.object_id = id;
    }


}