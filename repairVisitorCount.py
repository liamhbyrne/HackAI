from events_formatter import FormatEvents
import spacy

class EventEventComparator:
    def __init__(self, path="./data/events.csv"):
        fe = FormatEvents(path)
        fe.format_columns()
        self._events = fe.get_dataframe()
        self._nlp = spacy.load("en_core_web_sm")

    def clean(self):
        while -1 in self._events.visitors.unique():
            unclean_row = self._events[self._events.visitors == -1].head(1)
            unclean_type = unclean_row['type'].item()
            compare_to = self._nlp(unclean_row['description'].item())
            excluding = self._events.drop(unclean_row.index)
            mask = excluding.loc[(excluding['visitors'] != -1) & (excluding['type'] == unclean_type)]
            if not len(mask):
                mask = excluding.loc[(excluding['visitors'] != -1)]
            excluding['similarity'] = mask.apply(
                lambda row: compare_to.similarity(self._nlp(row.description)), axis=1
            )
            excluding = excluding.sort_values(by='similarity', ascending=False)
            print(unclean_row['description'].item())
            print(excluding[['description', 'similarity']])
            exhibitors, visitors = excluding[['exhibitors', 'visitors']].iloc[0]

            self._events.at[unclean_row.index.item(), 'visitors'] = visitors

        self._events.to_csv("clean.csv")
        return self._events


if __name__ == '__main__':
    r = EventEventComparator()
    r.clean()