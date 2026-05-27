import pygame
import calendar
import datetime
import json
import os

pygame.init()

# Цветовая палитра интерфейса
colorBackgroundApp = (11, 12, 16)
colorBackgroundPanel = (21, 22, 28)
colorBackgroundCell = (28, 29, 36)
colorBackgroundHover = (42, 43, 54)
colorBorderLine = (45, 46, 56)

# Цвета для текста
colorTextWhite = (255, 255, 255)
colorTextMuted = (140, 142, 155)
colorTextDark = (80, 82, 95)

# Акцентные цвета для видов спорта и заметок
colorF1 = (255, 40, 0)
colorF1Dim = (50, 15, 15)
colorBlue = (0, 229, 255)
colorBlueDim = (10, 45, 55)
colorFifa = (0, 210, 106)
colorFifaDim = (0, 50, 25)

# Подключение и настройка шрифтов
fontName = pygame.font.match_font(['inter', 'helvetica neue', 'segoe ui', 'roboto', 'arial'])
fontLogo = pygame.font.Font(fontName, 28)
fontLogo.set_bold(True)
fontTitle = pygame.font.Font(fontName, 42)
fontTitle.set_bold(True)
fontMid = pygame.font.Font(fontName, 24)
fontMid.set_bold(True)
fontBody = pygame.font.Font(fontName, 16)
fontSmall = pygame.font.Font(fontName, 13)
fontSmall.set_bold(True)
fontTiny = pygame.font.Font(fontName, 11)
fontTiny.set_bold(True)

# Локализация месяцев и дней недели
listMonths = ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
              "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
listMonthsGenitive = ["", "января", "февраля", "марта", "апреля", "мая", "июня",
                      "июля", "августа", "сентября", "октября", "ноября", "декабря"]
listWeekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

# Зафиксированное расписание Формулы 1
f1Schedule = {
    (2026, 3): {
        6: ["Практика 1", "Практика 2 (Австралия)"], 7: ["Практика 3", "Квалификация"], 8: ["Гонка: Австралия"],
        13: ["Практика 1", "Квал-я к спринту (Китай)"], 14: ["Спринт", "Основная квалификация"], 15: ["Гонка: Китай"],
        27: ["Практика 1", "Практика 2 (Япония)"], 28: ["Практика 3", "Квалификация"], 29: ["Гонка: Япония"]
    },
    (2026, 4): {
        10: ["Практика 1", "Практика 2 (Бахрейн)"], 11: ["Практика 3", "Квалификация"], 12: ["Гонка: Бахрейн"],
        17: ["Практика 1", "Практика 2 (Саудовская Аравия)"], 18: ["Практика 3", "Квалификация"],
        19: ["Гонка: Саудовская Аравия"]
    },
    (2026, 5): {
        1: ["Практика 1", "Квал-я к спринту (Майами)"], 2: ["Спринт", "Основная квалификация"], 3: ["Гонка: Майами"],
        22: ["Практика 1", "Квал-я к спринту (Канада)"], 23: ["Спринт", "Основная квалификация"], 24: ["Гонка: Канада"]
    },
    (2026, 6): {
        5: ["Практика 1", "Практика 2 (Монако)"], 6: ["Практика 3", "Квалификация"], 7: ["Гонка: Монако"],
        12: ["Практика 1", "Практика 2 (Испания)"], 13: ["Практика 3", "Квалификация"], 14: ["Гонка: Испания"],
        26: ["Практика 1", "Квал-я к спринту (Австрия)"], 27: ["Спринт", "Основная квалификация"],
        28: ["Гонка: Австрия"]
    },
    (2026, 7): {
        3: ["Практика 1", "Практика 2 (Великобритания)"], 4: ["Практика 3", "Квалификация"],
        5: ["Гонка: Великобритания"],
        17: ["Практика 1", "Практика 2 (Бельгия)"], 18: ["Практика 3", "Квалификация"], 19: ["Гонка: Бельгия"],
        24: ["Практика 1", "Практика 2 (Венгрия)"], 25: ["Практика 3", "Квалификация"], 26: ["Гонка: Венгрия"]
    },
    (2026, 8): {
        21: ["Практика 1", "Практика 2 (Нидерланды)"], 22: ["Практика 3", "Квалификация"], 23: ["Гонка: Нидерланды"]
    },
    (2026, 9): {
        4: ["Практика 1", "Практика 2 (Италия)"], 5: ["Практика 3", "Квалификация"], 6: ["Гонка: Италия"],
        11: ["Практика 1", "Практика 2 (Испания, Мадрид)"], 12: ["Практика 3", "Квалификация"], 13: ["Гонка: Мадрид"],
        25: ["Практика 1", "Практика 2 (Азербайджан)"], 26: ["Практика 3", "Квалификация"], 27: ["Гонка: Азербайджан"]
    },
    (2026, 10): {
        9: ["Практика 1", "Практика 2 (Сингапур)"], 10: ["Практика 3", "Квалификация"], 11: ["Гонка: Сингапур"],
        23: ["Практика 1", "Квал-я к спринту (США)"], 24: ["Спринт", "Основная квалификация"], 25: ["Гонка: Остин"],
        30: ["Практика 1", "Практика 2 (Мексика)"], 31: ["Практика 3", "Квалификация"]
    },
    (2026, 11): {
        1: ["Гонка: Мексика"],
        6: ["Практика 1", "Квал-я к спринту (Бразилия)"], 7: ["Спринт", "Основная квалификация"],
        8: ["Гонка: Бразилия"],
        19: ["Практика 1", "Практика 2 (Лас-Вегас)"], 20: ["Практика 3", "Квалификация"], 21: ["Гонка: Лас-Вегас"],
        27: ["Практика 1", "Квал-я к спринту (Катар)"], 28: ["Спринт", "Основная квалификация"], 29: ["Гонка: Катар"]
    },
    (2026, 12): {
        4: ["Практика 1", "Практика 2 (Абу-Даби)"], 5: ["Практика 3", "Квалификация"], 6: ["Гонка: Абу-Даби"]
    }
}

# Зафиксированное расписание Чемпионата мира по футболу
fifaSchedule = {
    (2026, 6): {
        11: ["Матч открытия (Мехико)"],
        12: ["Групповой этап"], 13: ["Групповой этап"], 14: ["Групповой этап"], 15: ["Групповой этап"],
        16: ["Групповой этап"], 17: ["Групповой этап"], 18: ["Групповой этап"], 19: ["Групповой этап"],
        20: ["Групповой этап"], 21: ["Групповой этап"], 22: ["Групповой этап"], 23: ["Групповой этап"],
        24: ["Групповой этап"], 25: ["Групповой этап"], 26: ["Групповой этап"], 27: ["Групповой этап"],
        28: ["1/16 финала"], 29: ["1/16 финала"], 30: ["1/16 финала"]
    },
    (2026, 7): {
        1: ["1/16 финала"], 2: ["1/16 финала"], 3: ["1/16 финала"],
        4: ["1/8 финала"], 5: ["1/8 финала"], 6: ["1/8 финала"], 7: ["1/8 финала"],
        9: ["1/4 финала"], 10: ["1/4 финала"], 11: ["1/4 финала"],
        14: ["Полуфинал"], 15: ["Полуфинал"],
        18: ["Матч за 3-е место (Майами)"],
        19: ["Финал (Нью-Йорк / Нью-Джерси)"]
    }
}


# Главный класс приложения
class CalendarApplication:
    def __init__(self):
        # Настройки окна и названия приложения
        monitorInfo = pygame.display.Info()
        self.windowWidth = monitorInfo.current_w
        self.windowHeight = monitorInfo.current_h
        self.displayScreen = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Календарь")

        # Имя файла для сохранения пользовательских данных
        self.dataFile = "events.json"
        self.userEvents = self.loadEvents()

        # Текущее время и вкладки
        timeNow = datetime.datetime.now()
        self.currentYear = timeNow.year
        self.currentMonth = timeNow.month
        self.dateToday = timeNow
        self.selectedDay = timeNow.day

        self.inputActive = False
        self.userText = ""
        self.activeTab = "Календарь"
        self.isFullscreen = False
        self.isRunning = True

        # Контейнеры для возврата интерактивных зон
        self.buttonLeft = None
        self.buttonRight = None
        self.listDayButtons = []
        self.rectangleInput = None
        self.listDeleteButtons = []
        self.listMenuRectangles = []

    # Загрузка локальных записей пользователя
    def loadEvents(self):
        if os.path.exists(self.dataFile):
            try:
                with open(self.dataFile, "r", encoding="utf-8") as fileObject:
                    fileData = json.load(fileObject)
                    return {tuple(map(int, key.split('-'))): value for key, value in fileData.items()}
            except:
                return {}
        return {}

    # Сохранение записей пользователя на диск
    def saveEvents(self):
        dictionaryData = {f"{key[0]}-{key[1]}-{key[2]}": value for key, value in self.userEvents.items()}
        with open(self.dataFile, "w", encoding="utf-8") as fileObject:
            json.dump(dictionaryData, fileObject, ensure_ascii=False, indent=4)

    # Отрисовка скругленных прямоугольников
    def drawRoundedRect(self, surfaceObject, colorValue, rectangleObject, radiusValue=12, widthValue=0):
        pygame.draw.rect(surfaceObject, colorValue, rectangleObject, border_radius=radiusValue, width=widthValue)

    # Создание плавающей панели с эффектом падающей тени
    def drawPanel(self, surfaceObject, rectangleObject, radiusValue=20):
        shadowOffset = 8
        shadowSurface = pygame.Surface((rectangleObject.w + shadowOffset * 2, rectangleObject.h + shadowOffset * 2),
                                       pygame.SRCALPHA)
        pygame.draw.rect(shadowSurface, (0, 0, 0, 40),
                         (shadowOffset, shadowOffset, rectangleObject.w, rectangleObject.h), border_radius=radiusValue)
        surfaceObject.blit(shadowSurface, (rectangleObject.x - shadowOffset, rectangleObject.y - shadowOffset + 5))

        self.drawRoundedRect(surfaceObject, colorBackgroundPanel, rectangleObject, radiusValue)
        self.drawRoundedRect(surfaceObject, colorBorderLine, rectangleObject, radiusValue, 1)

    # Создание маленьких тегов для обозначения событий
    def drawPillBadge(self, surfaceObject, textString, positionX, positionY, backgroundColor, textColor):
        textSurface = fontTiny.render(textString.upper(), True, textColor)
        paddingX, paddingY = 16, 8
        badgeHeight = textSurface.get_height() + paddingY
        badgeRectangle = pygame.Rect(positionX, positionY, textSurface.get_width() + paddingX, badgeHeight)

        self.drawRoundedRect(surfaceObject, backgroundColor, badgeRectangle, badgeHeight // 2)
        self.drawRoundedRect(surfaceObject, textColor, badgeRectangle, badgeHeight // 2, 1)

        surfaceObject.blit(textSurface, textSurface.get_rect(center=badgeRectangle.center))
        return badgeRectangle.height

    # Основная функция отрисовки всего интерфейса
    def renderInterface(self, mousePosition):
        self.displayScreen.fill(colorBackgroundApp)

        self.listMenuRectangles = []
        self.listDayButtons = []
        self.listDeleteButtons = []
        self.buttonLeft = None
        self.buttonRight = None
        self.rectangleInput = None

        # Вычисление размеров ключевых зон экрана
        paddingValue = 24
        panelHeight = self.windowHeight - paddingValue * 2
        widthLeft = 240
        widthRight = 380
        widthMiddle = self.windowWidth - widthLeft - widthRight - paddingValue * 4

        rectangleMenu = pygame.Rect(paddingValue, paddingValue, widthLeft, panelHeight)
        rectangleCentral = pygame.Rect(rectangleMenu.right + paddingValue, paddingValue, widthMiddle, panelHeight)
        rectangleRightPanel = pygame.Rect(rectangleCentral.right + paddingValue, paddingValue, widthRight, panelHeight)

        # Отрисовка левого навигационного меню
        self.drawPanel(self.displayScreen, rectangleMenu)

        # Размещение логотипа приложения
        pygame.draw.circle(self.displayScreen, colorF1, (rectangleMenu.x + 35, rectangleMenu.y + 45), 8)
        pygame.draw.circle(self.displayScreen, colorFifa, (rectangleMenu.x + 35, rectangleMenu.y + 65), 8)
        logoSurface = fontLogo.render("HUB 2026", True, colorTextWhite)
        self.displayScreen.blit(logoSurface, (rectangleMenu.x + 55, rectangleMenu.y + 35))
        pygame.draw.line(self.displayScreen, colorBorderLine, (rectangleMenu.x + 24, rectangleMenu.y + 100),
                         (rectangleMenu.right - 24, rectangleMenu.y + 100), 1)

        # Размещение навигационных кнопок в меню
        listMenuNames = ["Календарь", "Сезон 2026", "ЧМ 2026", "Мои Заметки"]
        positionY = rectangleMenu.y + 130

        for itemText in listMenuNames:
            itemRectangle = pygame.Rect(rectangleMenu.x + 16, positionY, widthLeft - 32, 48)
            isActive = (itemText == self.activeTab)

            if isActive:
                self.drawRoundedRect(self.displayScreen, colorBackgroundHover, itemRectangle, 12)
                pygame.draw.rect(self.displayScreen, colorBlue, (itemRectangle.x + 12, itemRectangle.y + 14, 4, 20),
                                 border_radius=2)
                currentColor = colorTextWhite
                offsetX = 32
            else:
                if itemRectangle.collidepoint(mousePosition):
                    self.drawRoundedRect(self.displayScreen, colorBackgroundCell, itemRectangle, 12)
                    currentColor = colorTextWhite
                else:
                    currentColor = colorTextMuted
                offsetX = 24

            textSurface = fontBody.render(itemText, True, currentColor)
            self.displayScreen.blit(textSurface, (itemRectangle.x + offsetX, itemRectangle.y + 14))
            self.listMenuRectangles.append((itemRectangle, itemText))
            positionY += 56

        # Отрисовка экрана при активной вкладке Календарь
        if self.activeTab == "Календарь":
            self.drawPanel(self.displayScreen, rectangleCentral)

            # Вывод месяца и года
            headerSurface = fontTitle.render(f"{listMonths[self.currentMonth]} {self.currentYear}", True,
                                             colorTextWhite)
            self.displayScreen.blit(headerSurface, (rectangleCentral.x + 40, rectangleCentral.y + 35))

            # Отрисовка кнопок перелистывания календаря
            buttonSize = 44
            arrowPositionY = rectangleCentral.y + 35 + headerSurface.get_height() // 2 - buttonSize // 2
            self.buttonLeft = pygame.Rect(rectangleCentral.right - 120, arrowPositionY, buttonSize, buttonSize)
            self.buttonRight = pygame.Rect(rectangleCentral.right - 60, arrowPositionY, buttonSize, buttonSize)

            for buttonObject, listPoints in [(self.buttonLeft, [(-4, 0), (4, -6), (4, 6)]),
                                             (self.buttonRight, [(4, 0), (-4, -6), (-4, 6)])]:
                isHover = buttonObject.collidepoint(mousePosition)
                self.drawRoundedRect(self.displayScreen, colorBackgroundHover if isHover else colorBackgroundCell,
                                     buttonObject, buttonSize // 2)
                self.drawRoundedRect(self.displayScreen, colorBorderLine, buttonObject, buttonSize // 2, 1)
                centerX, centerY = buttonObject.center
                realPoints = [(centerX + pointX, centerY + pointY) for pointX, pointY in listPoints]
                pygame.draw.polygon(self.displayScreen, colorTextWhite if isHover else colorTextMuted, realPoints)

            # Подготовка параметров календарной сетки
            gridPositionY = rectangleCentral.y + 120
            cellWidth = (rectangleCentral.w - 80) // 7
            cellHeight = (rectangleCentral.h - 150) // 6

            # Вывод названий дней недели над сеткой
            for indexDay, stringDay in enumerate(listWeekdays):
                daySurface = fontSmall.render(stringDay.upper(), True, colorTextMuted)
                centerPositionX = rectangleCentral.x + 40 + indexDay * cellWidth + cellWidth // 2
                self.displayScreen.blit(daySurface, daySurface.get_rect(center=(centerPositionX, gridPositionY - 20)))

            # Загрузка чисел текущего месяца и выборки событий
            calendarData = calendar.monthcalendar(self.currentYear, self.currentMonth)
            currentF1Events = f1Schedule.get((self.currentYear, self.currentMonth), {})
            currentFifaEvents = fifaSchedule.get((self.currentYear, self.currentMonth), {})

            # Построение ячеек календаря
            for indexRow, currentWeek in enumerate(calendarData):
                for indexColumn, numberDay in enumerate(currentWeek):
                    cellRectangle = pygame.Rect(rectangleCentral.x + 40 + indexColumn * cellWidth + 6,
                                                gridPositionY + indexRow * cellHeight + 6, cellWidth - 12,
                                                cellHeight - 12)

                    if numberDay != 0:
                        isToday = (
                                    numberDay == self.dateToday.day and self.currentMonth == self.dateToday.month and self.currentYear == self.dateToday.year)
                        isSelected = (self.selectedDay == numberDay)
                        isHover = cellRectangle.collidepoint(mousePosition)

                        # Изменение фона ячейки при наведении или отметке текущего дня
                        if isToday:
                            self.drawRoundedRect(self.displayScreen, colorBlueDim, cellRectangle, 16)
                            self.drawRoundedRect(self.displayScreen, colorBlue, cellRectangle, 16, 2)
                        else:
                            self.drawRoundedRect(self.displayScreen,
                                                 colorBackgroundHover if isHover else colorBackgroundCell,
                                                 cellRectangle, 16)
                            self.drawRoundedRect(self.displayScreen, colorBorderLine, cellRectangle, 16, 1)

                        # Рисование белой рамки для выбранной даты
                        if isSelected and not isToday:
                            self.drawRoundedRect(self.displayScreen, colorTextWhite, cellRectangle, 16, 2)

                        # Вывод номера дня
                        colorNumber = colorBlue if isToday else colorTextWhite
                        numberSurface = fontMid.render(str(numberDay), True, colorNumber)
                        self.displayScreen.blit(numberSurface, (cellRectangle.x + 16, cellRectangle.y + 12))

                        tagPositionY = cellRectangle.y + 44

                        # Вставка тегов при совпадении с расписанием автоспорта
                        if numberDay in currentF1Events:
                            tagHeight = self.drawPillBadge(self.displayScreen, "F1 Сессия", cellRectangle.x + 16,
                                                           tagPositionY, colorF1Dim, colorF1)
                            tagPositionY += tagHeight + 6

                        # Вставка тегов при совпадении с расписанием футбола
                        if numberDay in currentFifaEvents:
                            tagHeight = self.drawPillBadge(self.displayScreen, "ЧМ 2026", cellRectangle.x + 16,
                                                           tagPositionY, colorFifaDim, colorFifa)
                            tagPositionY += tagHeight + 6

                        # Вывод тегов наличия пользовательских заметок
                        listUserEntries = self.userEvents.get((self.currentYear, self.currentMonth, numberDay), [])
                        if listUserEntries:
                            countText = f"{len(listUserEntries)} Заметк{'а' if len(listUserEntries) == 1 else 'и'}"
                            self.drawPillBadge(self.displayScreen, countText, cellRectangle.x + 16, tagPositionY,
                                               colorBlueDim, colorBlue)

                        self.listDayButtons.append((cellRectangle, numberDay))

            # Отрисовка правой информационной панели
            self.drawPanel(self.displayScreen, rectangleRightPanel)

            if self.selectedDay:
                # Вывод заголовка выбранной даты
                numberLargeSurface = fontTitle.render(str(self.selectedDay), True, colorTextWhite)
                monthLargeSurface = fontMid.render(f"{listMonthsGenitive[self.currentMonth]} {self.currentYear}", True,
                                                   colorTextMuted)

                isTodaySelected = (
                            self.selectedDay == self.dateToday.day and self.currentMonth == self.dateToday.month and self.currentYear == self.dateToday.year)
                if isTodaySelected:
                    self.drawPillBadge(self.displayScreen, "СЕГОДНЯ", rectangleRightPanel.x + 32,
                                       rectangleRightPanel.y + 35, colorBlueDim, colorBlue)
                    offsetPositionY = rectangleRightPanel.y + 65
                else:
                    offsetPositionY = rectangleRightPanel.y + 35

                self.displayScreen.blit(numberLargeSurface, (rectangleRightPanel.x + 32, offsetPositionY))
                self.displayScreen.blit(monthLargeSurface, (
                rectangleRightPanel.x + 32 + numberLargeSurface.get_width() + 10, offsetPositionY + 12))
                pygame.draw.line(self.displayScreen, colorBorderLine,
                                 (rectangleRightPanel.x + 32, offsetPositionY + 60),
                                 (rectangleRightPanel.right - 32, offsetPositionY + 60), 1)
                contentPositionY = offsetPositionY + 85

                # Отображение списка сессий Формулы 1 на выбранный день
                if self.selectedDay in currentF1Events:
                    labelSurface = fontSmall.render("РАСПИСАНИЕ F1", True, colorF1)
                    self.displayScreen.blit(labelSurface, (rectangleRightPanel.x + 32, contentPositionY))
                    contentPositionY += 25
                    for sessionText in currentF1Events[self.selectedDay]:
                        cardRectangle = pygame.Rect(rectangleRightPanel.x + 32, contentPositionY, widthRight - 64, 48)
                        self.drawRoundedRect(self.displayScreen, colorBackgroundApp, cardRectangle, 12)
                        pygame.draw.rect(self.displayScreen, colorF1, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                         border_radius=2)
                        sessionSurface = fontBody.render(sessionText, True, colorTextWhite)
                        self.displayScreen.blit(sessionSurface, (cardRectangle.x + 16, cardRectangle.y + 14))
                        contentPositionY += 52
                    contentPositionY += 12

                # Отображение футбольных матчей на выбранный день
                if self.selectedDay in currentFifaEvents:
                    labelSurface = fontSmall.render("ФУТБОЛ ЧМ 2026", True, colorFifa)
                    self.displayScreen.blit(labelSurface, (rectangleRightPanel.x + 32, contentPositionY))
                    contentPositionY += 25
                    for sessionText in currentFifaEvents[self.selectedDay]:
                        cardRectangle = pygame.Rect(rectangleRightPanel.x + 32, contentPositionY, widthRight - 64, 48)
                        self.drawRoundedRect(self.displayScreen, colorBackgroundApp, cardRectangle, 12)
                        pygame.draw.rect(self.displayScreen, colorFifa, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                         border_radius=2)
                        sessionSurface = fontBody.render(sessionText, True, colorTextWhite)
                        self.displayScreen.blit(sessionSurface, (cardRectangle.x + 16, cardRectangle.y + 14))
                        contentPositionY += 52
                    contentPositionY += 12

                # Вывод всех добавленных пользователем заметок
                listUserEntries = self.userEvents.get((self.currentYear, self.currentMonth, self.selectedDay), [])
                labelNotesSurface = fontSmall.render("ЗАМЕТКИ", True, colorBlue)
                self.displayScreen.blit(labelNotesSurface, (rectangleRightPanel.x + 32, contentPositionY))
                contentPositionY += 25

                if listUserEntries:
                    for indexEntry, stringEntry in enumerate(listUserEntries):
                        cardRectangle = pygame.Rect(rectangleRightPanel.x + 32, contentPositionY, widthRight - 64, 48)
                        isHover = cardRectangle.collidepoint(mousePosition)
                        self.drawRoundedRect(self.displayScreen,
                                             colorBackgroundHover if isHover else colorBackgroundApp, cardRectangle, 12)
                        if isHover: self.drawRoundedRect(self.displayScreen, colorBorderLine, cardRectangle, 12, 1)
                        pygame.draw.rect(self.displayScreen, colorBlue, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                         border_radius=2)

                        displayText = stringEntry if fontBody.size(stringEntry)[
                                                         0] < cardRectangle.width - 50 else stringEntry[:22] + "..."
                        textSurface = fontBody.render(displayText, True, colorTextWhite)
                        self.displayScreen.blit(textSurface, (cardRectangle.x + 16, cardRectangle.y + 14))

                        # Отрисовка интерактивного крестика для удаления заметки
                        deleteRectangle = pygame.Rect(cardRectangle.right - 36, cardRectangle.y + 14, 20, 20)
                        if isHover:
                            deleteColor = colorF1 if deleteRectangle.collidepoint(mousePosition) else colorTextMuted
                            pygame.draw.line(self.displayScreen, deleteColor,
                                             (deleteRectangle.left + 4, deleteRectangle.top + 4),
                                             (deleteRectangle.right - 4, deleteRectangle.bottom - 4), 2)
                            pygame.draw.line(self.displayScreen, deleteColor,
                                             (deleteRectangle.right - 4, deleteRectangle.top + 4),
                                             (deleteRectangle.left + 4, deleteRectangle.bottom - 4), 2)
                        self.listDeleteButtons.append((deleteRectangle, indexEntry))
                        contentPositionY += 52
                else:
                    emptySurface = fontBody.render("Записей пока нет", True, colorTextDark)
                    self.displayScreen.blit(emptySurface, (rectangleRightPanel.x + 32, contentPositionY))

                # Поле для ввода текста новой заметки внизу панели
                self.rectangleInput = pygame.Rect(rectangleRightPanel.x + 32, rectangleRightPanel.bottom - 80,
                                                  widthRight - 64, 48)
                self.drawRoundedRect(self.displayScreen, colorBackgroundApp, self.rectangleInput, 24)
                self.drawRoundedRect(self.displayScreen, colorBlue if self.inputActive else colorBorderLine,
                                     self.rectangleInput, 24, 2 if self.inputActive else 1)

                hintText = "Добавить запись (Enter)..." if not self.userText and not self.inputActive else self.userText
                textColor = colorTextWhite if self.userText else colorTextMuted
                displayHintText = hintText if fontBody.size(hintText)[
                                                  0] < self.rectangleInput.width - 40 else "..." + hintText[-25:]
                self.displayScreen.blit(fontBody.render(displayHintText, True, textColor),
                                        (self.rectangleInput.x + 20, self.rectangleInput.y + 14))

            else:
                # Заглушка, отображаемая при пустом выборе дня
                messageSurface = fontMid.render("Выберите дату", True, colorTextWhite)
                subtitleSurface = fontBody.render("чтобы увидеть расписание", True, colorTextMuted)
                self.displayScreen.blit(messageSurface, messageSurface.get_rect(
                    center=(rectangleRightPanel.centerx, rectangleRightPanel.centery - 10)))
                self.displayScreen.blit(subtitleSurface, subtitleSurface.get_rect(
                    center=(rectangleRightPanel.centerx, rectangleRightPanel.centery + 20)))

        # Отрисовка экрана при активной вкладке Сезон F1
        elif self.activeTab == "Сезон 2026":
            self.drawPanel(self.displayScreen, rectangleCentral)
            headerSurface = fontTitle.render("Гран-при Формулы 1 (2026)", True, colorTextWhite)
            self.displayScreen.blit(headerSurface, (rectangleCentral.x + 40, rectangleCentral.y + 35))

            self.drawPanel(self.displayScreen, rectangleRightPanel)
            rightHeader = fontTitle.render("Статистика F1", True, colorTextWhite)
            self.displayScreen.blit(rightHeader, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 35))

            listAllRaces = []
            for monthKey, daysDictionary in f1Schedule.items():
                yearValue, monthValue = monthKey
                for dayValue, sessionsList in daysDictionary.items():
                    for sessionString in sessionsList:
                        if "Гонка" in sessionString:
                            listAllRaces.append((monthValue, dayValue, sessionString))

            listAllRaces.sort(key=lambda item: (item[0], item[1]))

            positionX = rectangleCentral.x + 40
            positionY = rectangleCentral.y + 110
            columnWidth = (rectangleCentral.w - 100) // 2

            # Отрисовка гонок списком в две колонки
            for indexValue, raceItem in enumerate(listAllRaces):
                currentX = positionX if indexValue < 12 else positionX + columnWidth + 20
                currentY = positionY + (indexValue % 12) * 56
                cardRectangle = pygame.Rect(currentX, currentY, columnWidth, 48)
                self.drawRoundedRect(self.displayScreen, colorBackgroundCell, cardRectangle, 12)
                pygame.draw.rect(self.displayScreen, colorF1, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                 border_radius=2)
                dateSurface = fontBody.render(f"{raceItem[1]:02d}.{raceItem[0]:02d}", True, colorTextMuted)
                self.displayScreen.blit(dateSurface, (cardRectangle.x + 16, cardRectangle.y + 14))
                raceSurface = fontBody.render(raceItem[2].replace("Гонка: ", "").strip(), True, colorTextWhite)
                self.displayScreen.blit(raceSurface, (cardRectangle.x + 80, cardRectangle.y + 14))

            statsSurface1 = fontBody.render(f"Всего этапов: {len(listAllRaces)}", True, colorTextWhite)
            self.displayScreen.blit(statsSurface1, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 110))

        # Отрисовка экрана при активной вкладке ЧМ 2026
        elif self.activeTab == "ЧМ 2026":
            self.drawPanel(self.displayScreen, rectangleCentral)
            headerSurface = fontTitle.render("Чемпионат мира по футболу 2026", True, colorTextWhite)
            self.displayScreen.blit(headerSurface, (rectangleCentral.x + 40, rectangleCentral.y + 35))

            self.drawPanel(self.displayScreen, rectangleRightPanel)
            rightHeader = fontTitle.render("Главные этапы", True, colorTextWhite)
            self.displayScreen.blit(rightHeader, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 35))

            # Выборка матчей стадии плей-офф и матча открытия
            listAllMatches = []
            for monthKey, daysDictionary in fifaSchedule.items():
                yearValue, monthValue = monthKey
                for dayValue, sessionsList in daysDictionary.items():
                    for sessionString in sessionsList:
                        if "Групповой" not in sessionString:
                            listAllMatches.append((monthValue, dayValue, sessionString))

            listAllMatches.sort(key=lambda item: (item[0], item[1]))

            positionX = rectangleCentral.x + 40
            positionY = rectangleCentral.y + 110
            columnWidth = (rectangleCentral.w - 100) // 2

            # Отрисовка футбольных матчей списком в две колонки
            for indexValue, matchItem in enumerate(listAllMatches):
                currentX = positionX if indexValue < 10 else positionX + columnWidth + 20
                currentY = positionY + (indexValue % 10) * 56
                cardRectangle = pygame.Rect(currentX, currentY, columnWidth, 48)
                self.drawRoundedRect(self.displayScreen, colorBackgroundCell, cardRectangle, 12)
                pygame.draw.rect(self.displayScreen, colorFifa, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                 border_radius=2)
                dateSurface = fontBody.render(f"{matchItem[1]:02d}.{matchItem[0]:02d}", True, colorTextMuted)
                self.displayScreen.blit(dateSurface, (cardRectangle.x + 16, cardRectangle.y + 14))
                matchSurface = fontBody.render(matchItem[2], True, colorTextWhite)
                self.displayScreen.blit(matchSurface, (cardRectangle.x + 80, cardRectangle.y + 14))

            statsSurface1 = fontBody.render("Всего матчей турнира: 104", True, colorTextWhite)
            statsSurface2 = fontBody.render("США, Канада, Мексика", True, colorTextMuted)
            self.displayScreen.blit(statsSurface1, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 110))
            self.displayScreen.blit(statsSurface2, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 140))

        # Отрисовка экрана при активной вкладке Мои Заметки
        elif self.activeTab == "Мои Заметки":
            self.drawPanel(self.displayScreen, rectangleCentral)
            headerSurface = fontTitle.render("Недавние записи", True, colorTextWhite)
            self.displayScreen.blit(headerSurface, (rectangleCentral.x + 40, rectangleCentral.y + 35))

            self.drawPanel(self.displayScreen, rectangleRightPanel)
            rightHeader = fontTitle.render("Инфо", True, colorTextWhite)
            self.displayScreen.blit(rightHeader, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 35))

            # Формирование единого списка всех сохраненных заметок пользователя
            listAllNotes = []
            for dateKey, notesList in self.userEvents.items():
                for noteString in notesList:
                    listAllNotes.append((dateKey, noteString))

            listAllNotes.sort(key=lambda item: (item[0][0], item[0][1], item[0][2]), reverse=True)

            positionY = rectangleCentral.y + 110
            for noteItem in listAllNotes:
                # Прерывание отрисовки, чтобы карточки не выходили за нижнюю границу окна
                if positionY > rectangleCentral.bottom - 70:
                    break

                cardRectangle = pygame.Rect(rectangleCentral.x + 40, positionY, rectangleCentral.w - 80, 48)
                self.drawRoundedRect(self.displayScreen, colorBackgroundCell, cardRectangle, 12)
                pygame.draw.rect(self.displayScreen, colorBlue, (cardRectangle.x, cardRectangle.y + 10, 4, 28),
                                 border_radius=2)
                dateKey = noteItem[0]
                dateSurface = fontBody.render(f"{dateKey[2]:02d}.{dateKey[1]:02d}.{dateKey[0]}", True, colorTextMuted)
                self.displayScreen.blit(dateSurface, (cardRectangle.x + 16, cardRectangle.y + 14))
                noteSurface = fontBody.render(noteItem[1], True, colorTextWhite)
                self.displayScreen.blit(noteSurface, (cardRectangle.x + 120, cardRectangle.y + 14))
                positionY += 56

            statsSurface1 = fontBody.render(f"Всего заметок: {len(listAllNotes)}", True, colorTextWhite)
            self.displayScreen.blit(statsSurface1, (rectangleRightPanel.x + 32, rectangleRightPanel.y + 110))

    # Запуск и поддержание работы программы
    def runApplication(self):
        while self.isRunning:
            mousePosition = pygame.mouse.get_pos()
            self.renderInterface(mousePosition)
            pygame.display.flip()

            # Цикл обработки действий пользователя
            for eventObject in pygame.event.get():
                if eventObject.type == pygame.QUIT:
                    self.isRunning = False

                # Динамическая обработка изменения размеров окна
                elif eventObject.type == pygame.VIDEORESIZE:
                    if not self.isFullscreen:
                        self.windowWidth, self.windowHeight = eventObject.w, eventObject.h
                        self.displayScreen = pygame.display.set_mode((self.windowWidth, self.windowHeight),
                                                                     pygame.RESIZABLE)

                # Проверка нажатий кнопок мыши
                elif eventObject.type == pygame.MOUSEBUTTONDOWN:
                    if eventObject.button == 1:
                        # Переключение активной вкладки через левое меню
                        clickedMenu = False
                        for menuRectangle, menuName in self.listMenuRectangles:
                            if menuRectangle.collidepoint(mousePosition):
                                self.activeTab = menuName
                                clickedMenu = True
                                break

                        if clickedMenu:
                            continue

                        if self.activeTab == "Календарь":
                            # Проверка кликов по кнопкам удаления заметок
                            deletedSomething = False
                            for deleteRectangle, entryIndex in self.listDeleteButtons:
                                hitboxRectangle = deleteRectangle.inflate(10, 10)
                                if hitboxRectangle.collidepoint(mousePosition):
                                    dateKey = (self.currentYear, self.currentMonth, self.selectedDay)
                                    self.userEvents[dateKey].pop(entryIndex)
                                    if not self.userEvents[dateKey]:
                                        del self.userEvents[dateKey]
                                    self.saveEvents()
                                    deletedSomething = True
                                    break

                            if deletedSomething:
                                continue

                            # Обработка нажатий на стрелки переключения месяца
                            if self.buttonLeft and self.buttonLeft.collidepoint(mousePosition):
                                self.currentMonth -= 1
                                if self.currentMonth < 1:
                                    self.currentMonth = 12
                                    self.currentYear -= 1
                                self.selectedDay = None
                            elif self.buttonRight and self.buttonRight.collidepoint(mousePosition):
                                self.currentMonth += 1
                                if self.currentMonth > 12:
                                    self.currentMonth = 1
                                    self.currentYear += 1
                                self.selectedDay = None
                            else:
                                # Проверка клика по конкретному дню в сетке
                                clickedDay = False
                                for cellRectangle, numberDay in self.listDayButtons:
                                    if cellRectangle.collidepoint(mousePosition):
                                        self.selectedDay = numberDay
                                        self.inputActive = False
                                        clickedDay = True
                                        break

                                # Активация поля для ввода текста заметки
                                if self.rectangleInput and self.rectangleInput.collidepoint(mousePosition):
                                    self.inputActive = True
                                elif not clickedDay:
                                    self.inputActive = False

                # Проверка нажатий на клавиатуре
                elif eventObject.type == pygame.KEYDOWN:
                    # Включение и отключение полноэкранного режима
                    if eventObject.key == pygame.K_F11:
                        self.isFullscreen = not self.isFullscreen
                        if self.isFullscreen:
                            self.displayScreen = pygame.display.set_mode((self.windowWidth, self.windowHeight),
                                                                         pygame.FULLSCREEN)
                        else:
                            self.displayScreen = pygame.display.set_mode((self.windowWidth, self.windowHeight),
                                                                         pygame.RESIZABLE)

                    # Сброс фокуса ввода или закрытие программы
                    elif eventObject.key == pygame.K_ESCAPE:
                        if self.inputActive:
                            self.inputActive = False
                        elif self.selectedDay:
                            self.selectedDay = None
                        else:
                            self.isRunning = False

                    # Логика ввода текста в активное поле
                    elif self.inputActive and self.selectedDay and self.activeTab == "Календарь":
                        if eventObject.key == pygame.K_RETURN:
                            if self.userText.strip():
                                dateKey = (self.currentYear, self.currentMonth, self.selectedDay)
                                if dateKey not in self.userEvents:
                                    self.userEvents[dateKey] = []
                                self.userEvents[dateKey].append(self.userText.strip())
                                self.saveEvents()
                                self.userText = ""
                        elif eventObject.key == pygame.K_BACKSPACE:
                            self.userText = self.userText[:-1]
                        else:
                            if len(self.userText) < 60:
                                self.userText += eventObject.unicode

        # Освобождение ресурсов при выходе
        pygame.quit()


if __name__ == "__main__":
    appInstance = CalendarApplication()
    appInstance.runApplication()