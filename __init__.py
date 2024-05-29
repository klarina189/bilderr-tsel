from otree.api import *
import itertools

class C(BaseConstants):
    NAME_IN_URL = 'identify_paintings'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    id_treatment_label = models.StringField()
    group_label = models.StringField()
    price_sharing_rule = models.StringField()
    group_number = models.IntegerField()
    painting_1 = models.IntegerField(
        label='Kunstwerk 1',
        choices=[[0, "Salvador Dalí"], [0, 'René Magritte'], [1, 'Joan Miró'],
                 [0, 'Robert Motherwell'], [0, 'Jackson Pollock']],
        widget=widgets.RadioSelect
    )
    painting_2 = models.IntegerField(
        label='Kunstwerk 2',
        choices=[[1, "Sandro Boticelli"], [0, 'Leonardo da Vinci'], [0, 'Michelangelo'],
                 [0, 'Raphael'], [0, 'Titian']],
        widget=widgets.RadioSelect
    )
    painting_3 = models.IntegerField(
        label='Kunstwerk 3',
        choices=[[0, "Thomas Hart Benton"], [0, 'Jon Steuart Curry'], [0, 'Alexandre Hogue'],
                 [0, 'Edna Reindel'], [1, 'Grant Wood']],
        widget=widgets.RadioSelect
    )
    painting_4 = models.IntegerField(
        label='Kunstwerk 4',
        choices=[[0, "Francis Bacon"], [0, 'Salvador Dalí'], [0, 'Édouard Monet'],
                 [0, 'Pablo Picasso'], [1, 'Diego Velázquez']],
        widget=widgets.RadioSelect
    )
    circle_question_bf_PGG = models.IntegerField(
        label='Bitte sehen Sie sich das Diagramm mit den Kreisen an. Überlegen Sie nun,'
              ' welches dieser Kreispaare Ihre Verbindung zu Ihrem*Ihrer Gruppenpartner*in,'
              ' am besten repräsentiert. Bitte geben Sie durch Auswahl der entsprechenden'
              ' Grafik unten an, inwieweit Sie glauben, dass Sie und diese Person miteinander'
              ' verbunden sind.',
        widget=widgets.RadioSelectHorizontal,
        choices=[[0, '<img src=" /static/Self_Other_0.jpg" alt="Image 0">'],
                 [1, '<img src=" /static/Self_Other_1.jpg" alt="Image 1">'],
                 [2, '<img src=" /static/Self_Other_2.jpg" alt="Image 2">'],
                 [3, '<img src=" /static/Self_Other_3.jpg" alt="Image 3">'],
                 [4, '<img src=" /static/Self_Other_4.jpg" alt="Image 1">'],
                 [5, '<img src=" /static/Self_Other_5.jpg" alt="Image 2">'],
                 [6, '<img src=" /static/Self_Other_6.jpg" alt="Image 3">']
                 ],
    )
    we_question_bf_PGG = models.IntegerField(
        label='Bitte kreuzen Sie nun an, inwieweit Sie den Begriff "WIR" verwenden würden,'
              ' um von Ihnen und Ihrem*Ihrer Gruppenpartner*in zu sprechen.',
        min=0,
        max=7,
        widget=widgets.RadioSelectHorizontal,
        choices=[0, 1, 2, 3, 4, 5, 6, 7],
    )
    amount_correct_answers = models.IntegerField()
    channel_name = models.StringField()
    channel_nickname = models.StringField()
    payoff_SPT = models.CurrencyField()



# FUNCTIONS
def set_channel_name(p, group_id):
    """To be alligned with the second part of the experiment, the participants are grouped into teams of four,
    already in this stage. But to only allow the people being actually in the same group. This function sets the
     channel names and nicknames for the subgroups."""
    if p.id_in_group == 1:
        channel_name = f'{group_id}_A'
        nickname = 'Teilnehmer*in 1'
    elif p.id_in_group == 2:
        channel_name = f'{group_id}_A'
        nickname = 'Teilnehmer*in 2'
    elif p.id_in_group == 3:
        channel_name = f'{group_id}_B'
        nickname = 'Teilnehmer*in 1'
    else:
        channel_name = f'{group_id}_B'
        nickname = 'Teilnehmer*in 2'
    return channel_name, nickname


def creating_session(subsession):
    """This functions clusters the players and groups depending on group
       affiliation and price sharing rule. As two different price sharing
       rules (egalitarian = EPS and proportional = PPS) are used, it is
       precisely these that are allocated at group level. In addition,
       subgroups are formed, so that these subgroups (A or B) can compete
       against each other in their large group. Additionally it is determined
       whether the groups play in the high or low identity treatment. The groups
       have the conditions (both EPS or PPS and both high ID or low ID). The
       characteristics are set on participant level, so that they can be used
       in the second part of this expeirment."""
    if subsession.round_number == 1:
        id_treatment_options = itertools.cycle(["LowID", "LowID", "LowID", "LowID",
                                                "HighID", "HighID", "HighID", "HighID"])
        group_label_options = itertools.cycle(["A", "A", "B", "B"])
        price_sharing_options = itertools.cycle(["EPS", "EPS", "EPS", "EPS",
                                                 "EPS", "EPS", "EPS", "EPS",
                                                 "PPS", "PPS", "PPS", "PPS",
                                                 "PPS", "PPS", "PPS", "PPS"])
        for player in subsession.get_players():
            participant = player.participant
            participant.id_treatment_label = next(id_treatment_options)
            participant.group_label = next(group_label_options)
            participant.price_sharing_rule = next(price_sharing_options)
            participant.group_number = player.group.id_in_subsession
            player.channel_name, player.channel_nickname = set_channel_name(player, player.group.id_in_subsession)



def det_correct_answers(player1, player2):
    """This function determines the amount of correct answers for the paintings, correctly identified
    in the social proximity (identity task). As the players only receive points, if their assigned partner
    gave the correct answer too, this function checks whether this is the case or not."""
    if player1.painting_1 + player2.painting_1 == 2:
        painting_1_answer = 1
    else:
        painting_1_answer = 0
    if player1.painting_2 + player2.painting_2 == 2:
        painting_2_answer = 1
    else:
        painting_2_answer = 0
    if player1.painting_3 + player2.painting_3 == 2:
        painting_3_answer = 1
    else:
        painting_3_answer = 0
    if player1.painting_4 + player2.painting_4 == 2:
        painting_4_answer = 1
    else:
        painting_4_answer = 0
    amount_correct_answers = painting_1_answer + painting_2_answer +\
                             painting_3_answer + painting_4_answer
    return amount_correct_answers


def set_payoffs(group: Group):
    """This function sets the payoff based on the amount of correct answers."""
    for player in group.get_players():
        if player.participant.group_label == 'A':
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            player.amount_correct_answers = det_correct_answers(p1, p2)
        elif player.participant.group_label == 'B':
            p3 = group.get_player_by_id(3)
            p4 = group.get_player_by_id(4)
            player.amount_correct_answers = det_correct_answers(p3, p4)
        player.payoff = player.amount_correct_answers * 40
        player.participant.payoff_SPT = player.payoff


# PAGES
class Instruktionen_IdentifyPaintings(Page):
    pass

class ResultsWaitPage(WaitPage):
    title_text = "Bitte warten"
    body_text = "Bitte warten Sie bis die anderen Teilnehmer*innen bereit sind. Es kann sein, dass Sie etwas länger" \
                " auf andere Personen warten müssen. Das ist kein Fehler, sondern Teil des Spiels."


class IdentifyPaintings(Page):
    form_model = 'player'
    form_fields = ['painting_1', 'painting_2', 'painting_3', 'painting_4']
    timeout_seconds = 300


class ResultsWaitPage1(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text = "Bitte warten"
    body_text = "Bitte warten Sie bis die anderen Teilnehmer*innen bereit sind. Es kann sein, dass Sie etwas länger" \
                " auf andere Personen warten müssen. Das ist kein Fehler, sondern Teil des Spiels."

class Results(Page):
    pass


class SocialProximityQuestion(Page):
    form_model = 'player'
    form_fields = ['circle_question_bf_PGG', 'we_question_bf_PGG']


page_sequence = [Instruktionen_IdentifyPaintings, ResultsWaitPage, IdentifyPaintings,
                 ResultsWaitPage1, Results, SocialProximityQuestion]
