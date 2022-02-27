import { THIS_EXPR } from "@angular/compiler/src/output/output_ast";

export class ProblemInformationPick {
    difficulty = '';
    title = '';
    tags: Array<String> = new Array<String>();
    num: number = 0;
    object_id: string = '';
    start_time: string = '';
    end_time: string = '';
    is_active: boolean = true;
    time_limit: string = "";

    get_time_limit_string(): string{
        if (this.time_limit === '-1'){
            return "Няма";
        }
        else{
            return this.time_limit;
        }
    }

    parse_difficulty(diff: string): string {
        switch (diff) {
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

    get_tags(): string {
        return this.tags.join(", ").toString();
    }

    get_active(): string {
        if (this.is_active) {
            return "Да";
        }
        else {
            return "Не";
        }
    }

    constructor(
        num: number = 0,
        title: string = "",
        difficulty: string = "",
        tags: Array<any> = [],
        id: string = "",
        start_time: string = "",
        end_time: string = "",
        is_active: boolean = true,
        time_limit: string = ""
    ) {
        this.difficulty = this.parse_difficulty(difficulty);
        this.title = title;
        this.tags = tags;
        this.num = num;
        this.object_id = id;
        this.start_time = start_time;
        this.end_time = end_time;
        this.is_active = is_active;
        this.time_limit = time_limit;

    }


}