<?php

use Symfony\Component\Console\Application;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Helper\ProgressBar;

$app['dolibarr'] = new Dolibarr($app);

$console = new Application('BDE cotisation', 'n/a');
$console->getDefinition()->addOption(new InputOption('--env', '-e', InputOption::VALUE_REQUIRED, 'The Environment name.', 'dev'));
$console->setDispatcher($app['dispatcher']);
$console
    ->register('import')
    ->setDefinition(array(
        new InputOption('file', null, InputOption::VALUE_REQUIRED, 'Adresse du fichier cotisant'),
    ))
    ->setDescription('Import fichier de cotisant. Le fichier doit suivre le schéma suiviant: numéro étu, type de cotisation, montant')
    ->setCode(function (InputInterface $input, OutputInterface $output) use ($app) {

        $output->write("Chargement des mails ...");
        $renewHtml = $app['twig']->render('mails/renew.html.twig', array());
        $newHtml = $app['twig']->render('mails/new.html.twig', array());

        $output->write("Chargement des membres depuis picsou ... ");
        $members = $app['dolibarr']->getMembers();
        $dolibarr_link = [];
        $had_suscription = [];
        $mails = [];

        foreach ($members as $member)
        {
            if(isset($member['array_options']['options_student']))
            {
                $member_id = $member['id'];
                $member_student_id = $member['array_options']['options_student'];
                $dolibarr_link[$member_student_id] = $member_id;

                if($member['last_subscription_date'] != null)
                    $had_suscription[]= $member_student_id;

                if($member['email'] != null)
                    $mails[$member_student_id] = $member['email'];
            }
        }
        $output->writeln(count($dolibarr_link)." chargés");
        $import = "";

        $lignes = explode("\n", $import);
        $inconnu_user = [];
        $updated_user = [];
        $progress = new ProgressBar($output, count($lignes));
        $progress->start();
        foreach ($lignes as $ligne)
        {
            $ligne = explode(';', $ligne);
            if(count($ligne) >= 3)
            {
                $student_id = $ligne[0];
                if(isset($dolibarr_link[$student_id]))
                {
                    //$output->write('<info>Trouvé</info> ');
                    switch ($ligne[1])
                    {
                        case 'Année':
                            $req = $app['dolibarr']->createSubscriptionById($dolibarr_link[$student_id], '1 September 2018', strtotime('30 september 2019'), $ligne[2], 'Adhésion annuel (via UTT)');
                            break;
                        case 'Printemps':
                            $req = $app['dolibarr']->createSubscriptionById($dolibarr_link[$student_id], '1 February 2019', strtotime('30 september 2019'), $ligne[2], 'Adhésion semestre de printemps (via UTT)');
                            break;
                        case 'Automne':
                            $req = $app['dolibarr']->createSubscriptionById($dolibarr_link[$student_id], '1 September 2018', strtotime('01 february 2019'), $ligne[2], 'Adhésion semestre automne (via UTT)');
                            break;
                    }
                    if (!$req)
                    {
                        $output->write('<error>Suscription error '.$student_id.'</error> ');
                    } else {
                        // On envoi un mail
                        if (in_array($student_id, $had_suscription)) {
                            $message = (new Swift_Message())
                                ->setSubject('Bon retour au BDE !')
                                ->setFrom(array('bde@utt.fr'=> 'BDE UTT'))
                                ->setTo(array($mails[$student_id]))
                                ->addPart($renewHtml, 'text/html');
                        } else {
                            $message = (new Swift_Message())
                                ->setSubject('Bienvenue au BDE !')
                                ->setFrom(array('bde@utt.fr'=> 'BDE UTT'))
                                ->setTo(array($mails[$student_id]))
                                ->addPart($newHtml, 'text/html');
                        }
                        $app['mailer']->send($message);

                    }

                    $updated_user[] = $student_id;

                } else {
                    //$output->write('<error>Inconnu</error> ');
                    $inconnu_user[] = $student_id;
                }
                //$output->writeln("Etudiant n°".$ligne[0].' Periode: '.$ligne[1].' Montant: '.$ligne[2]);
                $progress->advance();
            }
        }

        $app['swiftmailer.spooltransport']
            ->getSpool()
            ->flushQueue($app['swiftmailer.transport'])
        ;

        $progress->finish();
        $output->writeln('<info>'.count($updated_user).' importés</info> <error>'.count($inconnu_user).' inconnu</error>');
        $output->writeln('<error>Inconnu: </error>'.implode(',', $inconnu_user));
        $output->writeln('<info>Ajouté: </info>'.implode(',', $updated_user));
        /**
        if (($handle = fopen($input->getOption('file'), "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 0, ";")) !== FALSE) {
                echo 'test';
                //$output->writeln("Etudiant n°".$data[0].' Periode: '.$data[1].' Montant: '.$data[2]);
            }
            fclose($handle);
        }**/
    })
;

return $console;
